-- Dummy data for USER table
INSERT INTO USER (UserFName, UserLName, UserEmail, UserPassword, Username) VALUES 
('John', 'Doe', 'john@ex.com', 'password1', 'johndoe'),
('Jane', 'Smith', 'jane@ex.com', 'password2', 'janesmith'),
('Michael', 'Johnson', 'michael@ex.com', 'password3', 'michaelj');

-- Dummy data for CLASS table
INSERT INTO CLASS (ClassName, ClassDescription, ClassBeffynessBonus, ClassSpeedinessBonus, ClassSmartnessBonus, ClassBuffnessBonus) VALUES 
('Warrior', 'A strong and tough fighter.', 5, 0, 1, 2),
('Rogue', 'A sneaky and agile character.', 1, 3, 1, 0),
('Wizard', 'A master of arcane knowledge.', 0, 1, 5, 0);

-- Dummy data for ITEM table
INSERT INTO ITEM (ItemCost, ItemName, ItemSpeedinessBonus, ItemSmartnessBonus, ItemBeefynessBonus, ItemBaseDamage) VALUES 
(10, 'Sword', 0, 0, 3, 8),
(5, 'Dagger', 2, 0, 0, 5),
(15, 'Staff', 0, 5, 0, 6);

-- Dummy data for RACE table
INSERT INTO RACE (RaceName, RaceDescription, RaceBuffnessBonus, RaceSmartnessBonus, RaceBeefynessBonus, RaceSpeedinessBonus) VALUES 
('Human', 'Versatile and adaptable.', 1, 1, 1, 1),
('Elf', 'Graceful and wise.', 0, 2, 0, 2),
('Dwarf', 'Tough and strong-willed.', 2, 0, 2, 0);

-- Dummy data for CHARACTERS table
INSERT INTO CHARACTERS (CharacterFName, CharacterLName, CharacterSmartness, CharacterBuffness, CharacterBeefyness, CharacterSpeediness, UserID, ClassID, RaceID) VALUES 
('Aragorn', 'Son of Arathorn', 4, 5, 5, 3, 1, 1, 1),
('Legolas', 'Greenleaf', 5, 2, 3, 5, 2, 2, 2),
('Gimli', 'Son of Gloin', 3, 5, 5, 2, 3, 1, 3);

-- Dummy data for Has table
INSERT INTO Has (ItemID, CharacterID) VALUES 
(1, 1),
(2, 2),
(3, 3);
