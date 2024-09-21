import signal, requests, os, json, time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as google_build

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

debugMode = True

# Stuff to gracefully handle SIGINT and SIGTERM
waitingToDie = False    # Is this true of my life?
def gracefullyDie(signum, frame):
  global waitingToDie
  print("Waiting to die gracefully...")
  waitingToDie = True

signal.signal(signal.SIGINT, gracefullyDie)
signal.signal(signal.SIGTERM, gracefullyDie)

def basePath():
  return os.path.dirname(os.path.abspath(__file__))

def getService():
  # token.pickle stores the user's access and refresh tokens
  try:
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  except:
    creds = None

  # We don't want the user login to happen from the indexer.
  # We only want to utilize valid credentials or refresh some.
  if not creds: return None
  if creds.expired and creds.refresh_token: creds.refresh(Request())
  if creds.valid: return google_build('drive', 'v3', credentials = creds)

  return None

def getIconPath(item):
    """Returns a file path for a file to use as the icon. May be None."""
    # No way to get an icon if it doesn't have one
    if ("mimeType" not in item) or ("iconLink" not in item):
        return None

    # Always create the icons folder if it doesn't exist
    os.makedirs("icons", exist_ok=True)

    # Check if the icon exists based on the mimeType
    iconPath = "icons/%s.png" % (item["mimeType"].replace("/", "-"))
    if os.path.exists(iconPath):
        return iconPath

    # Grab the icon from the iconLink if we can
    # Default link is to 16px version - get 128 cuz it aint 1993 boi
    r = requests.get(item["iconLink"].replace("/16/", "/128/"))
    open(iconPath, "wb").write(r.content)
    return iconPath

# Memoize to save time traversing the same parents, such as "My Drive"
# Looks like: {id: {isReadable: True|False, name: bla|None, realParentId: sdaf|None}}
knownFolderInfo = {}
def getFolderInfo(service, id):
  global knownFolderInfo

  if id in knownFolderInfo: return knownFolderInfo[id]

  try:
    result = service.files().get(fileId = id, fields="parents, name", supportsTeamDrives = True).execute()
  except:
    knownFolderInfo[id] = {"isReadable": False, "name": None, "realParentId": None}
    return knownFolderInfo[id]
  
  # Edge cases: there can be multiple parents and some files are their own parent
  # In the case of multiple parents, we select the first.
  # If the file is its own parent, it has no "Real" parent
  if "parents" in result and result["parents"][0] != id:
      realParentId = result["parents"][0]
  else:
      realParentId = None

  knownFolderInfo[id] = {"isReadable": True, "name": result["name"], "realParentId": realParentId}

  return knownFolderInfo[id]

def getFullParentList(service, parents):
  parentNameList = []

  currentParentId = parents[0]
  while not waitingToDie:
    folderInfo = getFolderInfo(service, currentParentId)
    
    # If we can't read it, then we can't do anything with it
    if not folderInfo["isReadable"]: break
    
    # Add it
    parentNameList.insert(0, folderInfo["name"])

    # Set up next iteration
    if folderInfo["realParentId"]:
      currentParentId = folderInfo["realParentId"]
    else:
      break

  return parentNameList

def updateCache(service):
  print("Updating local cache...")
  keywordFileFields = ["id", "name", "owners(displayName, emailAddress)", "sharingUser(displayName, emailAddress)"]
  generalFileFields = ["modifiedTime", "modifiedByMeTime", "viewedByMeTime", "mimeType", "createdTime", "webViewLink", "iconLink", "parents"]
  fileFields = keywordFileFields + generalFileFields
  fileFieldsStr = "files(%s)" % (", ".join(fileFields))
  fields = "nextPageToken, " + fileFieldsStr

  # Debug mode overrides
  pageSize = 10 if debugMode else 1000

  # Continuously query, adding to items
  nextPageToken = None
  itemCount = 0
  while not waitingToDie:
    result = service.files().list(
      includeTeamDriveItems = True,
      supportsTeamDrives = True,
      fields = fields,
      pageToken = nextPageToken,
      pageSize = pageSize,
      orderBy = "viewedByMeTime asc",
      q = "viewedByMeTime > '1970-01-01T00:00:00.000Z'"
    ).execute()

    if debugMode: json.dump(result, open("last_result.json", "w"), indent = 2)

    # Enrich with icon paths
    for item in result["files"]: item["iconPath"] = getIconPath(item)

    # Enrich with full parent tree
    for item in result["files"]:
      if "parents" in item:
        fullParentList = getFullParentList(service, item["parents"])

        if len(fullParentList) > 0: item["parentPath"] = " >> ".join(fullParentList)
        item.pop("parents") # Extra data, not needed

    itemCount += len(result["files"])
    print("Updating cache with %i more items, for %i total so far." % (len(result["files"]), itemCount))

    if not waitingToDie and not debugMode and "nextPageToken" in result:
        time.sleep(3)
        nextPageToken = result["nextPageToken"]
    else:
        return True

def main():
  os.chdir(basePath())
  print("Now in %s" % (os.getcwd()))

  open("temp.txt", "w").write("TESTINGOOOOOO")

  service = getService()
  if not service:
    print("No valid credentials found. Exiting.")
    exit(1)

  updateCache(service)
  print("Done.")
  exit(0)

if __name__ == '__main__':
  main()
