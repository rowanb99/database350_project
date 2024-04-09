CREATE TABLE USER
(
  UserID INT NOT NULL AUTO_INCREMENT,
  UserFName VARCHAR(25) NOT NULL,
  UserLName VARCHAR(25) NOT NULL,
  UserEmail VARCHAR(40) NOT NULL,
  UserPassword VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  Username VARCHAR(25) NOT NULL,
  PRIMARY KEY (UserID),
  UNIQUE (UserEmail),
  UNIQUE (Username)
);

CREATE TABLE CLASS
(
  ClassID INT NOT NULL AUTO_INCREMENT,
  ClassName VARCHAR(25) NOT NULL,
  ClassDescription VARCHAR(50) NOT NULL,
  ClassBeefynessBonus INT NOT NULL,
  ClassSpeedinessBonus INT NOT NULL,
  ClassSmartnessBonus INT NOT NULL,
  ClassBuffnessBonus INT NOT NULL,
  PRIMARY KEY (ClassID)
);

CREATE TABLE ITEM
(
  ItemID INT NOT NULL AUTO_INCREMENT,
  ItemCost INT NOT NULL,
  ItemName VARCHAR(25) NOT NULL,
  ItemSpeedinessBonus INT NOT NULL,
  ItemSmartnessBonus INT NOT NULL,
  ItemBeefynessBonus INT NOT NULL,
  ItemBaseDamage INT NOT NULL,
  PRIMARY KEY (ItemID)
);

CREATE TABLE RACE
(
  RaceID INT NOT NULL AUTO_INCREMENT,
  RaceName VARCHAR(25) NOT NULL,
  RaceDescription VARCHAR(50) NOT NULL,
  RaceBuffnessBonus INT NOT NULL,
  RaceSmartnessBonus INT NOT NULL,
  RaceBeefynessBonus INT NOT NULL,
  RaceSpeedinessBonus INT NOT NULL,
  PRIMARY KEY (RaceID)
);

CREATE TABLE CHARACTERS
(
  CharacterID INT NOT NULL AUTO_INCREMENT,
  CharacterFName VARCHAR(25) NOT NULL,
  CharacterLName VARCHAR(25) NOT NULL,
  CharacterSmartness INT NOT NULL,
  CharacterBuffness INT NOT NULL,
  CharacterBeefyness INT NOT NULL,
  CharacterSpeediness INT NOT NULL,
  UserID INT NOT NULL,
  ClassID INT NOT NULL,
  RaceID INT NOT NULL,
  EquippedItemID INT,
  CharacterPurse INT NOT NULL DEFAULT 50,
  PRIMARY KEY (CharacterID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID),
  FOREIGN KEY (ClassID) REFERENCES CLASS(ClassID),
  FOREIGN KEY (RaceID) REFERENCES RACE(RaceID),
  FOREIGN KEY (EquippedItemID) REFERENCES ITEM(ItemID)
);

CREATE TABLE CHARACTER_INVENTORY
(
  ItemID INT NOT NULL AUTO_INCREMENT,
  CharacterID INT NOT NULL,
  PRIMARY KEY (ItemID, CharacterID),
  FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID),
  FOREIGN KEY (CharacterID) REFERENCES CHARACTERS(CharacterID)
);

CREATE VIEW UserCredentialsView AS
SELECT Username, UserPassword
FROM user;

CREATE VIEW `ItemView` AS
SELECT ItemCost, ItemName, ItemSpeedinessBonus, ItemSmartnessBonus, ItemBeefynessBonus, ItemBaseDamage
FROM item;

CREATE VIEW CharacterInfo AS
SELECT UserID, CharacterID, CharacterFName, CharacterLName,
CharacterSmartness, CharacterBuffness, CharacterBeefyness, CharacterSpeediness,
ClassName,
ClassSmartnessBonus, ClassBuffnessBonus, ClassBeefynessBonus, ClassSpeedinessBonus,
RaceName,
RaceSmartnessBonus, RaceBuffnessBonus, RaceBeefynessBonus, RaceSpeedinessBonus,
ItemName,
ItemSmartnessBonus, ItemBeefynessBonus, ItemSpeedinessBonus
FROM characters
LEFT JOIN class
ON characters.ClassID = class.ClassID
LEFT JOIN race
ON characters.RaceID = race.RaceID
LEFT JOIN item
ON characters.EquippedItemID = item.ItemID;

CREATE VIEW Inventory AS
SELECT
characters.CharacterID, CharacterFName,
CharacterSmartness, CharacterBuffness, CharacterBeefyness, CharacterSpeediness,
item.ItemID, ItemName, ItemCost,
ItemSmartnessBonus, ItemBeefynessBonus, ItemSpeedinessBonus
FROM character_inventory
LEFT JOIN item
ON character_inventory.ItemID = item.ItemID
LEFT JOIN characters
ON character_inventory.CharacterID = characters.CharacterID;