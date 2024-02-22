CREATE TABLE USER
(
  UserEmail INT NOT NULL,
  UserFName INT NOT NULL,
  UserLName INT NOT NULL,
  UserPassword INT NOT NULL,
  Username INT NOT NULL,
  UserID INT NOT NULL,
  PRIMARY KEY (UserID),
  UNIQUE (UserEmail),
  UNIQUE (Username)
);

CREATE TABLE CLASS
(
  ClassName INT NOT NULL,
  ClassDescription INT NOT NULL,
  ClassID INT NOT NULL,
  ClassBeffynessBonus INT NOT NULL,
  ClassSpeedinessBonus INT NOT NULL,
  ClassSmartnessBonus INT NOT NULL,
  ClassBuffnessBonus INT NOT NULL,
  PRIMARY KEY (ClassID)
);

CREATE TABLE ITEM
(
  ItemID INT NOT NULL,
  ItemCost INT NOT NULL,
  ItemName INT NOT NULL,
  ItemSpeedinessBonus INT NOT NULL,
  ItemSmartnessBonus INT NOT NULL,
  ItemBeefynessBonus INT NOT NULL,
  ItemBaseDamage INT NOT NULL,
  PRIMARY KEY (ItemID)
);

CREATE TABLE RACE
(
  RaceID INT NOT NULL,
  RaceName INT NOT NULL,
  RaceDescription INT NOT NULL,
  RaceBuffnessBonus INT NOT NULL,
  RaceSmartnessBonus INT NOT NULL,
  RaceBeefynessBonus INT NOT NULL,
  RaceSpeedinessBonus INT NOT NULL,
  PRIMARY KEY (RaceID)
);

CREATE TABLE CHARACTERS
(
  CharacterID INT NOT NULL,
  CharacterFName INT NOT NULL,
  CharacterLName INT NOT NULL,
  CharacterSmartness INT NOT NULL,
  CharacterBuffness INT NOT NULL,
  CharacterBeefyness INT NOT NULL,
  CharacterSpeediness INT NOT NULL,
  UserID INT NOT NULL,
  ClassID INT NOT NULL,
  RaceID INT NOT NULL,
  PRIMARY KEY (CharacterID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID),
  FOREIGN KEY (ClassID) REFERENCES CLASS(ClassID),
  FOREIGN KEY (RaceID) REFERENCES RACE(RaceID)
);

CREATE TABLE Has
(
  ItemID INT NOT NULL,
  CharacterID INT NOT NULL,
  PRIMARY KEY (ItemID, CharacterID),
  FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID),
  FOREIGN KEY (CharacterID) REFERENCES CHARACTERS(CharacterID)
);
