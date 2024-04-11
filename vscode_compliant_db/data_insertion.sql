USE rpgdb;

INSERT INTO USER (UserFName, UserLName, UserEmail, UserPassword, Username) VALUES
('John', 'Doe', 'john@example.com', 'password123', 'johndoe'),
('Alice', 'Smith', 'alice@example.com', 'abc123', 'alice'),
('Bob', 'Johnson', 'bob@example.com', 'passbob', 'bobj'),
('Emily', 'Davis', 'emily@example.com', '123abc', 'emilyd'),
('Michael', 'Wilson', 'michael@example.com', 'ilovemike', 'mike'),
('Sarah', 'Brown', 'sarah@example.com', 'password456', 'sarahb'),
('David', 'Taylor', 'david@example.com', 'davidpass', 'davidt'),
('Jessica', 'Martinez', 'jessica@example.com', 'jesspass', 'jessica'),
('Daniel', 'Anderson', 'daniel@example.com', 'danpass', 'dan'),
('Olivia', 'Thomas', 'olivia@example.com', 'olivepass', 'oliviat');

INSERT INTO CLASS (ClassName, ClassDescription, ClassBeefynessBonus, ClassSpeedinessBonus, ClassSmartnessBonus, ClassBuffnessBonus) VALUES
('Warrior', 'Master of Combat', 5, 1, 2, 3),
('Mage', 'Wizard of Elements', 1, 2, 5, 3),
('Rogue', 'Shadow Assassin', 2, 5, 1, 3),
('Priest', 'Healer of the Light', 3, 1, 2, 5),
('Paladin', 'Champion of Justice', 4, 3, 2, 1),
('Ranger', 'Nature''s Guardian', 3, 4, 2, 1),
('Barbarian', 'Savage Brute', 5, 2, 1, 4),
('Bard', 'Melodious Troubadour', 2, 3, 4, 1),
('Sorcerer', 'Master of Arcana', 1, 2, 4, 3),
('Monk', 'Disciple of the Mind', 2, 3, 1, 5);

INSERT INTO ITEM (ItemCost, ItemName, ItemSpeedinessBonus, ItemSmartnessBonus, ItemBeefynessBonus, ItemBaseDamage) VALUES
(10, 'Sword', 1, 0, 3, 5),
(15, 'Staff', 0, 3, 1, 3),
(5, 'Dagger', 3, 1, 2, 2),
(20, 'Bow', 2, 2, 1, 4),
(8, 'Shield', 0, 2, 4, 0),
(12, 'Wand', 2, 4, 1, 2),
(18, 'Axe', 1, 1, 4, 5),
(25, 'Greatsword', 0, 0, 5, 7),
(30, 'Staff of Power', 0, 5, 0, 5),
(7, 'Rapier', 4, 2, 0, 3);

INSERT INTO RACE (RaceName, RaceDescription, RaceBuffnessBonus, RaceSmartnessBonus, RaceBeefynessBonus, RaceSpeedinessBonus) VALUES
('Human', 'Versatile Fighters', 2, 2, 2, 2),
('Elf', 'Agile and Wise', 1, 3, 1, 4),
('Dwarf', 'Resilient and Strong', 4, 1, 3, 1),
('Orc', 'Brutal and Fierce', 5, 0, 4, 2),
('Halfling', 'Nimble Tricksters', 1, 2, 0, 5),
('Gnome', 'Inventive Thinkers', 0, 4, 1, 3),
('Dragonborn', 'Dragon Descendants', 3, 2, 4, 1),
('Tiefling', 'Infernal Heritage', 2, 3, 1, 4),
('Half-Orc', 'Strong and Versatile', 4, 1, 3, 2),
('Half-Elf', 'Blended Ancestry', 2, 2, 1, 4);

INSERT INTO CHARACTERS (CharacterFName, CharacterLName, CharacterSmartness, CharacterBuffness, CharacterBeefyness, CharacterSpeediness, UserID, ClassID, RaceID, EquippedItemID) VALUES
('Mark', 'Johnson', 7, 5, 4, 3, 1, 1, 1, 1),
('Lisa', 'Thompson', 8, 3, 2, 1, 2, 2, 2, 2),
('Tom', 'Wilson', 5, 4, 3, 2, 3, 3, 3, 3),
('Emma', 'Brown', 6, 2, 5, 4, 4, 4, 4, 4),
('Ryan', 'Jones', 4, 3, 1, 5, 5, 5, 5, 5),
('Sophia', 'Clark', 6, 5, 4, 1, 6, 6, 6, 6),
('William', 'Lewis', 7, 4, 3, 2, 7, 7, 7, 7),
('Amelia', 'Allen', 5, 2, 1, 4, 8, 8, 8, 8),
('Lucas', 'Young', 4, 5, 3, 2, 9, 9, 9, 9),
('Mia', 'Wright', 6, 3, 2, 4, 10, 10, 10, 10);

INSERT INTO CHARACTER_INVENTORY (ItemID, CharacterID) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 4),
(7, 5),
(8, 6),
(9, 7),
(10, 8);