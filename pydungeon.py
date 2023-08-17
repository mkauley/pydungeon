# Import the various modules to be used by the game.
import boto3
import datetime
import json
import random 

# Define the database variables and the frequently used line/dash breaks
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
mydb = boto3.resource('dynamodb')
mytbl = 'pydungeon'
lineBreak = '=' * 60
dashBreak = '-' * 30

# Function to load JSON files into S3 buckets
def buckets():
    
    # Define initial elements
    myBucket = 'pydungeon'
    s3.create_bucket(Bucket=myBucket)

    # JSON Files Array
    files = ['pydungeon1.json', 'pydungeon2.json']
        
    # Loop through the files.
    for file in files:
        s3.upload_file(file, myBucket, file)

# All ASCII Art courtesy of:
# https://www.asciiart.eu/

# Banner ASCII art function
def artDragonBanner():
    print('        ,     \    /      ,         ')
    print('       / \    )\__/(     / \        ')
    print('      /   \  (_\  /_)   /   \       ')
    print(' ____/_____\__\@  @/___/_____\____  ')
    print('|             |\../|              | ')
    print('|              \VV/               | ')
    print('| Welcome to Cauley\'s pyDungeon!  |')
    print('|_________________________________| ')
    print(' |    /\ /      \ \      \ /\    |  ')
    print(' |  /   V        ))       V   \  |  ')
    print(' |/             //             \ |  ')
    print('                V                   ')
    return()
    
# Dragon Boss ASCII art function
def artDragon():
    print('A fierce dragon attacks you!                   ')
    print('\n      <>========()                           ') 
    print('     (/\___   /|\ \         ()===========<>_   ')
    print('           \_/ | \ \       / /|\   ______/ \)  ')
    print('             \_|  \       / / | \_/            ')
    print('               \|\/|\_   / /  /\/              ')
    print('                (oo)\ \_/ /  /                 ')
    print('               //_/\_\/  /  |                  ')
    print('              @@/  |=\   \  |                  ')
    print('                   \_=\_  \ |                  ')
    print('                     \==\  \|\_ snd            ')
    print('                  __(\===\(   )\               ')
    print('                 (((~) __(_/   |               ')
    print('                      (((~) \  /               ')
    print('                      ______/ /                ')
    print('                      \'------\'               ')
    return()
    
# Gryphon Boss ASCII art function
def artGryphon():
    print('An ancient Gryphon wakes and begins to attack!   ')
    print('\n             _____,    _..-=-=-=-=-====--,     ')
    print('          _.\'a   /  .-\',___,..=--=--==-\'      ')
    print('         ( _     \ /  //___/-=---=----\'         ')
    print('          ` `\    /  //---/--==----=-\'          ')
    print('       ,-.    | / \_//-_.\'==-==---=\'           ')
    print('      (.-.`\  | |\'../-\'=-=-=-=--\'             ')
    print('       (\' `\`\| //_|-\.`;-~````~,        _      ')
    print('            \ | \_,_,_\.\'        \     .\'_`\   ')
    print('             `\            ,    , \    || `\ \   ')
    print('               \    /   _.--\    \ \'._.\'/  / | ')
    print('               /  /`---\'   \ \   |`\'---\'   \/ ')
    print('              / /\'          \ ;-. \             ')
    print('     jgs   __/ /           __) \ ) `|            ')
    print('         ((=\'--;)         (,___/(,_/            ')
    return()
    
# Skeleton Minion ASCII art function
def artSkeleton():
    print('The dried bones of a skeleton move to attack you')
    print('\n                      ___                     ')
    print('                     (o.o)                      ')
    print('                      |=|                       ')
    print('                     __|__                      ')
    print('                  / /.=|=.\ \                   ')
    print('                 / / .=|=. \ \                  ')
    print('                 \ \ .=|=. / /                  ')
    print('                  \ \(_=_)/ /                   ')
    print('                    (:| |:)                     ')
    print('                     || ||                      ')
    print('                     () ()                      ')
    print('                     || ||                      ')
    print('                     || ||                      ')
    print('                l42 ==\' \'==                   ')
    return()

# Bat Swarm Boss ASCII art function
# It does not look very pretty hear because of all the escape characters used
# It looks great in the game though!
def artBatSwarm():
    print('The shrill cry of several bats descend upon you as a bat swarm attacks!   ')
    print('    =/\                   /\=                                             ')
    print('    /  \ \'._  (\_/)   _.\'/  \       (_                   _)             ')
    print('   /    .''._\'--(o.o)--\'_.''.    \       /\                 /\          ')
    print('  / .\' _/ |`\'=/ " \=\'`| \_  `.\     / \'._    (\_/)   _.\'/ \          ')
    print(' / ` .\' `\;-,\'\___/\',-;/` \' . \'\   /_.\'\'._\'--(\'.\')--\'_.\'\'._\ ')
    print('/ .-\' jgs   `\(-V-)/`        `-.\  | \_ / `;=/ " \=;` \ _/ |             ')
    print('              "   "                \/  `\__|`\___/`|__/`  \/              ')
    print('                                    `       \(/|\)/        `              ')
    print('                                             " ` "                        ')
    print(lineBreak)
    return ()
    
# Since this program uses a lot of menu's, this function dynamically builds
# Them from an array passed into the function. It also auto-enumerates the lists
def blankMenu(menuArray):
    for idx, obj in enumerate(menuArray, 1):
        print(f"{idx}. {obj}")
    print(dashBreak)
    return()

# This function populates the initial default table values from JSON
# Whenever a new game is started, these weill be rerun.
def addRecordsFromJson():
    # I was running into issues with errors where the table contents could
    # not be loaded. This was because DynamoDB had not finished creating the 
    # table so I added in this waiter to not move forward until the table exists.
    # Sadly, it does slow things down a bit.
    dynamodb.get_waiter('table_exists').wait(TableName=mytbl)
    
    # An array of all the JSON files used. They will need to be in the same
    # Directory as the Python program.
    fileArray = ['pydungeon1.json', 'pydungeon2.json']
    
    # Loop through the JSON files in the array and load each.
    for each in fileArray:
        f = open(each)
        request_items = json.loads(f.read())
        response = dynamodb.batch_write_item(RequestItems=request_items)
    return()

# This builds the initial table to be populated.    
def buildTable():
    
    table = dynamodb.create_table(
        TableName=mytbl,
        KeySchema=[
            {
                # attrId is the key pair used for the table.
                'AttributeName': 'attrId',
                'KeyType': 'HASH'  
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'attrId', 
                'AttributeType': 'S'
            }, 
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    
    return()

# This drops the table so that a new game can be started. 
def dropTable():
    print('...Clearing Out Previous Data. Please Wait..........')
    
    # Delete Dynamo DB table
    dynamodb.delete_table(TableName=mytbl)
    dynamodb.get_waiter('table_not_exists').wait(TableName=mytbl)
    
    print('...Data Purge Completed.............................')
    
    myBucket = 'pydungeon'
    
    # Delete S3 bucket
    s3.delete_object(Bucket=myBucket, Key='pydungeon1.json')
    s3.delete_object(Bucket=myBucket, Key='pydungeon2.json')
    s3.delete_bucket(Bucket=myBucket)
    return()

# This checks to see if the table exists, returning a True of False
def checkTable():
    allTables = dynamodb.list_tables()['TableNames']
    if mytbl in allTables:
        print('...Pre-existing Data Present........................')
        return True
    else:
        return False

# Checks to see if the table exists, if it does, it drops it.
# Then rebuilds the table
def newTable():
    if checkTable():
        dropTable()
    
    buildTable()
    print('...New Game Initialized.............................')
    print('...Adding Default Game Data.........................')
    
    # Also runs the function to populate the newly built table.
    addRecordsFromJson()
    
    return ()

# Since getting data from the table is a common need in the program,
# this is a function to pull single values out of the table by passing in
# The key ID and the name of the attribute to retrieve.
def getter(rId, attrName):
    table = mydb.Table(mytbl)
    
    queriedVal = table.get_item(Key={'attrId': rId})
    
    item = queriedVal.get('Item')
    if item:
        return item.get(attrName)
    else:
        return None

# As equally important as getting data is setting or updating it.
# Likewise, a function built to update a record in the table based on the
# Key ID, attribute name, and new value.
def setter(rId, attrName, newVal):
    tableVal = mydb.Table(mytbl)
    
    # Performs the update.
    tableVal.update_item(
        Key={'attrId': rId},
        UpdateExpression='SET #attrName = :updVal',
        ExpressionAttributeValues={':updVal': newVal},
        ExpressionAttributeNames={'#attrName': attrName}
    )
    
# A function to move from one room to the next and also update the 
# "Save Point". This way, if the player wants to exit the game and
# continue later, they can.
def roomSelect(chosenType, chosenId, oId):
    if chosenType == 'move':
        # Updates the save point data.
        setter('SVPT', 'currRoom', chosenId)
        buildRoom(chosenId, oId)
        return()
    elif chosenType == 'quit':
        startMenu()
        return()

# The combat module! This is a huge function as there is a lot to do.    
def fightMe(rId, oId):
    
    # A dictionary to look up the ASCII art functions and matches to the monster.
    artFunctionDictionary = {
        'Skeleton': artSkeleton,
        'Bat Swarm': artBatSwarm,
        'Gryphon': artGryphon,
        'Dragon': artDragon
    }
    
    # All the monster ID's are cleverly built to be 'NPC' plus the room they are in.
    monsterId = 'NPC' + rId
    
    # Defining my table data.
    tableVal = mydb.Table(mytbl)

    qryMeTable = tableVal.get_item(Key={'attrId': 'PC1'})
    item = qryMeTable.get('Item')
    
    # Getting all the information on the player character (PC) to be used
    if item:
        myHealth = item.get('curHealth')
        myAttkPwr = item.get('attkPower')
        myArmor = item.get('armorLevel')
        myDamage = item.get('damage')

    qryThemTable = tableVal.get_item(Key={'attrId': monsterId})
    item = qryThemTable.get('Item')
    
    # Getting all the information on the monster (NPC) to be used in the fight.
    if item:
        itsHealth = item.get('curHealth')
        itsFullHealth = item.get('maxHealth')
        itsAttkPwr = item.get('attkPower')
        itsArmor = item.get('armorLevel')
        itsDamage = item.get('damage')
        monsterName = item.get('charName')
        monsterDesc = monsterName + ' (' + item.get('charType') + ')'

    # A while true loop. This will keep the PC fighting the monster from one
    # round of play to the next.
    while True:
        
        # Once the monster's health hits zero, the fight is over. 
        # This updates the values to show the monster defeated and saves
        # any damage the player has taken.'
        if itsHealth is not None and itsHealth <= 0:
            setter(rId, 'monsterDefeated', 1)
            setter(monsterId, 'curHealth', itsHealth)
            setter('PC1', 'currHealth', myHealth)
            print(dashBreak)
            print('CONGRATULATIONS! THE MONSTER HAS BEEN DEFEATED!')
            break
        
        # Calls the ASCII art from the dictionary.
        monsterArt = artFunctionDictionary[monsterName]
        monsterArt()
        
        # Print out some details about the monster
        print(lineBreak)
        print(monsterDesc)
        print(lineBreak)
        
        # Print an interface taht shows the monster's and player's health.
        print('---PC Health: ' + str(myHealth) + '---Monster Health: ' + str(itsHealth) + '---' )
        
        # The fight menu.
        blankMenu(['Fight! (The monster makes an attack as well)', 'Run!', 'Exit to Main Menu' ])
        
        # The fight choices
        fightChoice = input('Choose your action: ')
        
        # What happens when you attack
        if fightChoice == '1':
            
            # A randomizer to see if you hit the monster.
            myAttack = myAttkPwr + random.randint(1,100)
    
            if myAttack >= itsArmor:
                itsHealth = itsHealth - myDamage
            
            # A randomizer to see if the monster hits you.
            itsAttack = itsAttkPwr + random.randint(1,100)
    
            if itsHealth > 0 and itsAttack >= myArmor:
                myHealth = myHealth - itsDamage
                
                # An if statement that tracks what happens when the player 
                # character dies / reaches zero hit points. 
                if myHealth <= 0:
                    print(dashBreak)
                    print('OH NO! YOU HAVE DIED!')
                    setter(monsterId, 'curHealth', itsFullHealth)
                    setter('PC1', 'curHealth', 1)
                    print(dashBreak)
                    # The player restarts the map at the beginning 
                    # with 1 hit point left
                    print('You have RESPAWNED at the beginning of the dungeon!')
                    print('You currently only have 1 Point of Health')
                    print(dashBreak)
                    buildRoom('A1','A1')
        
        # What happens when you run from a fight. You flee to the previous room.
        elif fightChoice == '2':
            setter(monsterId, 'curHealth', itsHealth)
            setter('PC1', 'currHealth', myHealth)
            buildRoom(oId, rId)
            
        # What happens when you exit the fight to the main menu.
        elif fightChoice == '3':
            setter(monsterId, 'curHealth', itsHealth)
            setter('PC1', 'currHealth', myHealth)
            startMenu()
    
    # After the fight is over, returns you to the room.
    buildRoom(rId, oId)
    return()

# A simple function to find the player's full health value and 
# restore them to that. 
def restUp(rId, oId):
    print('Your Health is now Fully Restored!')
    
    myMax = getter('PC1', 'maxHealth')
    setter('PC1', 'curHealth', myMax)
    
    buildRoom(rId, oId)
    return()

# The room search function    
def searchRoom(rId, oId):
    
    # Detemrine if it is flagged as already searched or not.
    cleared = str(getter(rId, 'searched'))

    # If already searched, tells you so.
    # By default, the JSON autofills rooms that have nothing in them as 
    # having already been searched.
    if cleared == '1':
        print('You find nothing of interest in the room.')
    
    # If not previously searched, will search the room.
    elif cleared == '0':
        setter(rId, 'searched', 1)
        
        # A series of IF/ELSE statements that determine what the player finds
        # in each of the searched rooms. 
        if rId == 'B5':
            print('You find a magic sword that increases you attack power!')
            setter('PC1', 'attkPower', 20)
        elif rId == 'B1':
            print('You discover a special potion that increases your damage!')
            setter('PC1', 'damage', 30)
        elif rId == 'E1':
            print('The treasure chest reveals a beautiful suit of armor that increases your armor level!')
            setter('PC1', 'armorLevel', 50)
        elif rId == 'E3':
            print('A good fairy enchants you! You are fully healed and your maximum health is increased!')
            setter('PC1', 'curHealth', 200)
            setter('PC1', 'maxHealth', 200)

        # Where as the others were all finding special items, this one actually 
        # alters the Dynamo DB entry for the room, changing the search option to
        # let the player go through the found hidden doorway.
        elif rId == 'E4':
            print('To the WEST lies a hidden door behind a bookcase that you almost missed!')
            setter('E4', 'menu3', 'Move West behind the hidden bookcase.')
            setter('E4', 'menu3Type', 'move')
        
        # When you search the final room after defeating the final boss, you
        # get some end credits!
        elif rId == 'E5':
            print('You find a secret door that finally lets you escape this horrible dungeon!')
            print('CONGRATULATIONS! YOU HAVE DEFEATED CAULEY\'S PYDUNGEON!')
            print('THANK YOU FOR PLAYING!')
            print(dashBreak)
            print('Code Written by Jeff Cauley \n UMGC - SDEV 400 - Secure Programming in the Cloud \n August 8, 2023')
            print(dashBreak)
            startMenu()
            
    # ...and once done searching, returns you to your room.    
    buildRoom(rId, oId)
        
    return()

# Another big function, this is the "room" function that allows you to interact
# with the rooms defined in the JSON/Dynamo DB
def buildRoom(rId, oId):
    print(lineBreak)

    # Basic table details
    tableVal = mydb.Table(mytbl)
    qryTable = tableVal.get_item(Key={'attrId': rId})
    item = qryTable.get('Item')
    
    # Actually go through the room
    if item:
        # Now that it's been entered, the room is tagged as "explored"
        setter(rId, 'explored', '1')
        
        # Get and populate the room description.
        desc = item.get('roomDesc')
        
        print(lineBreak)
        print('ROOM DESCRIPTION: ' + desc)
        print(dashBreak)

        # If there is a monster to fight, launchs the combat system.
        # Note, like the search function, the monsters are predefined in the
        # initial JSON. If there is a monster in the room, the defeated tag is
        # set to 0 and if there is not, it is default set to 1.
        if (item.get('monsterDefeated')) == 0:
            fightMe(rId, oId)
            return()
        
        # With the fighting out of the way, this will build the menu from
        # the data in the Dynamo DB
        else:
            menuObjs = [
                item.get('menu1'),
                item.get('menu2'),
                item.get('menu3'),
                item.get('menu4')
            ]
        
            blankMenu(menuObjs)
        
        # Variables to interact with the menu.
        roomChoice = input('\nSelect your choice (1-4): ')
        roomChoiceKey = f'menu{roomChoice}Type'
        roomChoiceValue = item.get(roomChoiceKey)
    
        # Move, Rest, and Search options.
        # Note the DB contains details about which direction leads to which room.
        if roomChoiceValue == 'move':
            newRoomKey = f'menu{roomChoice}NewId'
            newRoomId = item.get(newRoomKey)
            roomSelect(roomChoiceValue,newRoomId,rId)
            print('You have entered a different room: ')
        elif roomChoiceValue == 'rest':
            restUp(rId, oId)
        elif roomChoiceValue == 'search':
            searchRoom(rId, oId)
    
    return()  

# Function to exit program
def exit_program():
    
    # Provides the current date/time and thanks for playing.
    curDateTime = datetime.datetime.now()
    strDateTime = curDateTime.strftime('%Y-%m-%d %H:%M:%S')
    print('THANK YOU FOR PLAYING PYDUNGEON!')
    print('Exiting the program at %s' % strDateTime)
    exit()

# Function to navigate/display menu
def startMenu():
    startMenuVals = ['Start a New Game', 'Continue Game', 'Save and Exit', 'Exit Without Saving']

    print('\nMAIN MENU! MAKE A CHOICE, ADVENTURER!:\n')
    blankMenu(startMenuVals)
    
    # Navigation for the different game choices!
    choice = input('Enter your choice (1-4): ')

    if choice == '1':
        buckets()
        newTable()
        namer = input('Enter a name for your new character: ')
        setter('PC1', 'charName', namer)
        buildRoom('A1', 'A1')
    elif choice == '2':
        svPt = getter('SVPT', 'currRoom')
        buildRoom(svPt, 'A1')
    elif choice == '3':
        exit_program()
    elif choice == '4':
        dropTable()
        exit_program()
    else:
        print('Invalid choice. Please try again.')

# Main function
def main():
    artDragonBanner()
    
    while True:
        startMenu()
        
if __name__ == '__main__':
    main()