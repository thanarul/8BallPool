import phylib
import sqlite3
import os

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE 
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG 
MAX_TIME = phylib.PHYLIB_MAX_TIME 
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_RATE = 0.01

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
	"WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
	"""
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
	pass;


################################################################################
class StillBall( phylib.phylib_object ):
	"""
    Python StillBall class.
    """
	def __init__( self, number, pos ):
		"""
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
		phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
		self.__class__ = StillBall;


	# add an svg method here
	def svg(self):
            svg_string = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
                self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]
            )
            return svg_string


################################################################################

class Table( phylib.phylib_table ):
	"""
    Pool table class.
    """

	def __init__( self ):
		"""
		Table constructor method.
		This method call the phylib_table constructor and sets the current
        object index to -1.
        """
		phylib.phylib_table.__init__( self );
		self.current = -1;

	def __iadd__( self, other ):
		"""
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
		self.add_object( other );
		return self;
	
	def __iter__( self ):
		"""
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
		self.current = -1
		return self;
	
	def __next__( self ):
		"""
        This provides the next object from the table in a loop.
        """
		self.current += 1;  # increment the index to the next object
		if self.current < MAX_OBJECTS:   # check if there are no more objects
			return self[ self.current ]; # return the latest object

		# if we get there then we have gone through all the objects
		self.current = -1;    # reset the index counter
		raise StopIteration;  # raise StopIteration to tell for loop to stop

	def __getitem__( self, index ):
		"""
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
		result = self.get_object( index ); 
		if result==None:
			return None;
		if result.type == phylib.PHYLIB_STILL_BALL:
			result.__class__ = StillBall;
		if result.type == phylib.PHYLIB_ROLLING_BALL:
			result.__class__ = RollingBall;
		if result.type == phylib.PHYLIB_HOLE:
			result.__class__ = Hole;
		if result.type == phylib.PHYLIB_HCUSHION:
			result.__class__ = HCushion;
		if result.type == phylib.PHYLIB_VCUSHION:
			result.__class__ = VCushion;
		return result;
	
	def __str__( self ):
		"""
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
		result = "";    # create empty string
		result += "time = %6.1f;\n" % self.time;    # append time
		for i,obj in enumerate(self): # loop over all objects and number them
			result += "  [%02d] = %s\n" % (i,obj);  # append object description
		return result;  # return the string
		
	def segment( self ):
		"""
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """
		result = phylib.phylib_table.segment( self );
		if result:
			result.__class__ = Table;
			result.current = -1;
		return result;
		
	# add svg method here
	def svg(self):
		svg_String = HEADER
		for obj in self:
			if obj is not None:
				if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
					svg_String += f'<circle id="cue-ball" cx="{obj.obj.still_ball.pos.x}" cy="{obj.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="white" />\n'
				else:
					svg_String += obj.svg()
		svg_String += FOOTER
		return svg_String
		
	def roll( self, t ):
		new = Table();
		for ball in self:
			if isinstance( ball, RollingBall ):
				# create4 a new ball with the same number as the old ball
				new_ball = RollingBall( ball.obj.rolling_ball.number,
										Coordinate(0,0),
										Coordinate(0,0),
										Coordinate(0,0) );
				# compute where it rolls to
				phylib.phylib_roll( new_ball, ball, t );

				# add ball to table
				new += new_ball;

			if isinstance( ball, StillBall ):
					# create a new ball with the same number and pos as the old ball
					new_ball = StillBall( ball.obj.still_ball.number,
											Coordinate( ball.obj.still_ball.pos.x,
														ball.obj.still_ball.pos.y ) );
					# add ball to table
					new += new_ball;
			# return table
		return new;

	def cueBall(self):
		#finds the cue ball (ball number 0) in the table, and returns it if its found

		for ball in self:
			if isinstance(ball, RollingBall) and ball.obj.rolling_ball.number == 0:
				return (ball, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y)
			elif isinstance(ball, StillBall) and ball.obj.still_ball.number == 0: 
				return (ball, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)
		return None



class RollingBall(phylib.phylib_object):

    def __init__( self, number, pos, vel, acceleration): 

         # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acceleration, 
                                       0.0, 0.0 );
     # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;

        #svg method
    def svg(self): 

        svg_string = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]
        )
        return svg_string

class Hole(phylib.phylib_object): 
    def __init__( self, pos): 
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0 );
        self.__class__ = Hole;
        
        #svg method 
    
    def svg(self):
            svg_string = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (
                self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS
            )
            return svg_string



class HCushion(phylib.phylib_object):
    def __init__( self, y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y)
        self.__class__ = HCushion
        #svg methhod 
    
    def svg(self):
        ypos = -25 if self.obj.hcushion.y == 0 else 2700 
        svg_string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % ypos
        return svg_string

class VCushion(phylib.phylib_object):
    def __init__( self, x):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0 );
        self.__class__ = VCushion;

        #svg method 
    def svg(self): 
        xpos = -25 if self.obj.vcushion.x == 0 else 1350 
        svg_string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % xpos
        return svg_string

    

class Database:
	
	def __init__(self, reset=False):
		db_file = "phylib.db"
		## if reset is true delete file 
		if reset and os.path.exists(db_file):
			os.remove(db_file)

		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()
		if reset:
			self.createDB()

	#function to create tables
	def createDB(self):
		cursor = self.conn.cursor()
		# create the ball table 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Ball (
				BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				BALLNO INTEGER NOT NULL,
				XPOS FLOAT NOT NULL, 
				YPOS FLOAT NOT NULL, 
				XVEL FLOAT,
				YVEL FLOAT
			)
		""")
		# create the TTable 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS TTable (
				TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				TIME FLOAT NOT NULL 
			)
		""")

		# creating the BallTable
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS BallTable (
				BALLID INTEGER NOT NULL,
				TABLEID INTEGER NOT NULL,
				FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
				FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
			)
		""")

		# create the Shot table 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Shot (
				SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				PLAYERID INTEGER NOT NULL,
				GAMEID INTEGER NOT NULL,
				FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
				FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
			) 
		""")

		# create the TableShot Table 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS TableShot (
				TABLEID INTEGER NOT NULL,
				SHOTID INTEGER NOT NULL,
				FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
				FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
			)
		""")
		# create the Game table 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Game (
				GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				GAMENAME VARCHAR(64) NOT NULL 
			)
		""")
		#create the Player table
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Player (
				PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				GAMEID INTEGER NOT NULL,
				PLAYERNAME VARCHAR(64) NOT NULL,
				FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
			)
		""")

		self.conn.commit()
		cursor.close()

	def readTable(self, tableID):
		cur = self.conn.cursor()
		#retrieve time attribute from TTable 
		self.cursor.execute("SELECT * FROM TTable WHERE TABLEID = ?", (tableID + 1,))
		time = self.cursor.fetchone()
		
		if not time: 
			return None
		
		## create table object 
		table = Table()

		#assuming time is the second column in TTable 
		table.time = time[1] 

		# retrieve all the ball attributes 
		self.cursor.execute("""
			SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
			FROM Ball
			INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
			WHERE BallTable.TABLEID = ?""", (tableID + 1,))
		rows = self.cursor.fetchall()

		for time in rows:
			ballNo = time[1]
			#create the coordinate object for ball position 
			ballPosition = Coordinate(time[2], time[3])
			if time[4] is not None:
				ballVelocity = Coordinate(time[4], time[5])
				# calculate the speed 
				speed = (ballVelocity.x**2 + ballVelocity.y**2)**0.5
				## setting x and y acceleration to 0 
				xAcc = 0
				yAcc = 0

				if speed > VEL_EPSILON: 
					#calculate the opposite direction of velocity for drag force
					dragForceX = (-ballVelocity.x / speed)
					dragForceY = (-ballVelocity.y / speed)
					xAcc = dragForceX * DRAG
					yAcc = dragForceY * DRAG

				acceleration = Coordinate(xAcc, yAcc)
				# create rolling ball 
				ball = RollingBall(ballNo, ballPosition, ballVelocity, acceleration)
			else:
				# if no velocity create a still ball 
				ball = StillBall(ballNo, ballPosition)
			# add the object to the table 
			table += ball
		cur.close()
		return table
		

	def writeTable(self, table):

		cur = self.conn.cursor()
		# insert the time into table 
		cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
		# get the auto incremented table id value 
		tableID = cur.lastrowid
		# insert balls into ball and balltable 
		for ball in table: 
			if isinstance(ball, StillBall):
				cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?);", (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
				ballID = cur.lastrowid
				cur.execute("INSERT INTO BallTable (BALLID,TABLEID) VALUES (?, ?)", (ballID, tableID))
			elif isinstance(ball, RollingBall):
				cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
				ballID = cur.lastrowid
				cur.execute("INSERT INTO BallTable (BALLID,TABLEID) VALUES (?, ?)", (ballID, tableID))


		return tableID - 1

	def getGame(self, gameID):
		cur = self.conn.cursor()
		# retriving the game details from the database and returning a tuple with gameID, gameName, player1Name, player2Name 
		self.cursor.execute(""" 
			SELECT g.GAMENAME, p1.PLAYER1NAME, p2.PLAYER2NAME
			FROM GAME g
			JOIN Player p1 ON g.GAMEID = p1.GAMEID
			JOIN Player p2 on g.GAMEID = p2.GAMEID AND p1.PLAYERID < p2.PLAYERID 
			WHERE g.GAMEID = ? 
			""", (gameID))
		gameName, player1Name, player2Name = self.cursor.fetchone()
		self.conn.commit()
		cur.close()
		return gameID, gameName, player1Name, player2Name


	def setGame(self, gameName, player1Name, player2Name):
		cur = self.conn.cursor()
		# insert and set a new game into the database and returns new gameID 
		query = "INSERT into Game (GAMENAME) VALUES (?)"
		cur.execute(query, (gameName,))
		self.conn.commit()
		#retrieve gameID 
		cur.execute("SELECT GAMEID FROM Game WHERE GAMENAME=?", (gameName,))
		result = self.cursor.fetchone() 
		if result is None:
			gameID = 1
		gameID = result[0]
		# insert player records into the player table 
		self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
		self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

		self.conn.commit()
		cur.close()
		return gameID - 1



	def newShot(self, gameName, playerName):
		
		cur = self.conn.cursor()

		cur.execute("SELECT GAMEID FROM Game WHERE GAMENAME=?", (gameName,))
		result = cur.fetchone() 
		if result is None:
			gameID = 1
		gameID = result[0]

		#finding the playerID for the given playerName and Gameid
		cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME=? AND GAMEID=?", (playerName, gameID))
		result = cur.fetchone()
		if result is None: 
			gameID = 1
		
		playerID = result[0]

		#inserting the new shot entry 
		cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID))
		shotID = cur.lastrowid
		cur.close()
		return shotID

	def getLastTableID(self):
		self.cursor.execute("SELECT MAX(TABLEID) FROM TTable")
		result = self.cursor.fetchone()
		if result and result[0] is not None:
			return result[0]
		else:
			return 0   


	def close(self):
		self.conn.commit()
		self.conn.close()

class Game():

	def __init__(self, gameID = None, gameName=None, player1Name=None, player2Name=None):

		self.db = Database()
		if gameID is None and all([gameName, player1Name, player2Name]): 
			self.gameID = self.db.setGame(gameName, player1Name, player2Name)
			self.gameName = gameName
			self.player1Name = player1Name
			self.player2Name = player2Name

		elif gameID is not None:
			gameDetails = self.db.getGame(gameID)
			if gameDetails:
				self.gameID, self.gameName, self.player1Name, self.player2Name = gameDetails
			else:
				raise ValueError("error")
		else:
			raise TypeError("error")

	def shoot(self, gameName, playerName, table, xvel, yvel):

		db = Database()
		cur = db.conn.cursor()
		#add a shot entry and get the shotID 
		shotID = db.newShot(gameName, playerName)
		#find the cue ball
		cue_Ball, xpos, ypos = table.cueBall()
		if not cue_Ball:
			return None

		#storing the current position 
		xpos = cue_Ball.obj.still_ball.pos.x
		ypos = cue_Ball.obj.still_ball.pos.y

		# setting the cue ball attributes for a rolling ball
		cue_Ball.type = phylib.PHYLIB_ROLLING_BALL
		cue_Ball.obj.number = 0
		cue_Ball.obj.rolling_ball.pos.x = xpos
		cue_Ball.obj.rolling_ball.pos.y = ypos
		cue_Ball.obj.rolling_ball.vel.x = xvel
		cue_Ball.obj.rolling_ball.vel.y = yvel 
		# calculate the speed of the cue ball 
		speed = (xvel**2 + yvel**2)**0.5
		if speed > VEL_EPSILON:
			dragForceX = -xvel / speed
			dragForceY = -yvel / speed
			cue_Ball.obj.rolling_ball.acc.x = dragForceX * DRAG
			cue_Ball.obj.rolling_ball.acc.y = dragForceY * DRAG
		else:
			cue_Ball.obj.rolling_ball.acc.x = 0
			cue_Ball.obj.rolling_ball.acc.y = 0

		while table:
			startTime = table.time
			segment = table.segment()
			if segment is None:
				break
			segmentTime = segment.time - startTime
			frameCount = int(segmentTime / FRAME_RATE)
			for i in range(frameCount):
				frameTime = i * FRAME_RATE
				newTable = table.roll(frameTime)
				newTable.time = startTime + frameTime
				#save the table and record in tableshot
				tableID = db.writeTable(newTable)
				cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID + 1, shotID))
			# move to the next segment 
			table = segment
			startTime = segment.time

		self.conn.commit()
		# cur.close()
		# db.close()
		return tableID
