import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:


    def __init__(self,name,breed):
        self.id=None
        self.name=name
        self.breed=breed

    @classmethod
    def create_table(self):
        
        sql='''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY
            ,name TEXT
            ,breed TEXT
            )
        
        '''
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = '''
        DROP TABLE IF EXISTS dogs
        '''
        CURSOR.execute(sql)
        CONN.commit()
        
        
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        
    @classmethod
    def create(cls,name,breed):
        dog=Dog(name,breed)
        dog.save()
        
        sql="SELECT last_insert_rowid()"
        CURSOR.execute(sql)
        row_id=CURSOR.fetchone()[0]
        dog.id=row_id
        return dog
        
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = '''
        SELECT * FROM dogs
        '''
        all_dogs = CURSOR.execute(sql).fetchall()

        # Create a list to store Dog instances
        dog_instances = []
        for row in all_dogs:
            # Create a Dog instance for each row and append it to the list
            dog = cls.new_from_db(row)
            dog_instances.append(dog)
        
        return dog_instances
   
    @classmethod
    def find_by_name(cls, name):
        sql = '''
        SELECT * FROM dogs
        WHERE name = ?
        '''
        # Pass the name as a parameter to the execute method
        CURSOR.execute(sql, (name,))
        
        # Fetch the first matching row
        row = CURSOR.fetchone()
        
        # If no matching row found, return None
        if row is None:
            return None
        
        # Otherwise, create a Dog instance from the row and return it
        return cls.new_from_db(row)

    
    @classmethod
    def find_by_id(cls,id):
        sql='''
        SELECT * FROM dogs
        WHERE id = ?
        
        '''
        
        CURSOR.execute(sql,(id,))
        
        row=CURSOR.fetchone()
        
        if row is None:
            return None
        
        return cls.new_from_db(row)