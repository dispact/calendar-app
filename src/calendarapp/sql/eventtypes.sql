INSERT INTO eventtypes (name, color) VALUES
	('Personal', SELECT id FROM eventcolors WHERE name='Blue'),
	('Sick', SELECT id FROM eventcolors WHERE name='Red'),
	('Vacation', SELECT id FROM eventcolors WHERE name='Vacation')