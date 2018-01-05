#!python
"""
  Load tasks and resources from a file.
  Methods for tasks and resources
"""
from math import pi, cos, sin, sqrt
from json import load

class task( object ):
    """
    The task object
        id: unique ID
        location: location on the xy plane
        importance: currently 1, 2, 4, 8
        span: the [ minimum, nominal, maximum ] span for this task
        threshold: the minimum the distance metric of a slot can be to support the task
        distance: the [ minimum, nominal, maximum ] distance between task and resource
        characteristics: the resource must accept these characteristics
    """
    def __init__( self ):
        object.__init__( self )
        
        self.id = None
        self.location = None
        self.importance = None
        self.threshold = None
        self.span = [ ]
        self.distance = [ ]
        self.characteristics = [ ]

    def self.getid( self ):
        return( self.id )

    def self.getloc( self ):
        return( self.id )

    def self.getimp( self ):
        return( self.id )

    def self.getthr( self ):
        return( self.id )

    def self.getspan( self ):
        return( self.id )

    def self.getdist( self ):
        return( self.id )

    def self.getchar( self ):
        return( self.id )

    def setAttributes( self, ID, Attrib ):
        """
        Assigns the attributes from the json file to the task
        """
        self.id = ID
        self.location, self.importance, self.span, self.threshold, \
            self.distance, self.characteristics = Attrib

class rsrc( object ):
    """
    The rsrc object
        id: unique ID
        location: location on the xy plane
        importance: currently 1, 2, 4, 8
        span: the [ minimum, nominal, maximum ] span for this rsrc
        threshold: the minimum the distance metric of a slot can be to support the rsrc
        distance: the [ minimum, nominal, maximum ] distance between rsrc and resource
        characteristics: the resource must accept these characteristics
    """
    def __init__( self ):
        object.__init__( self )
        
        self.id = None
        self.position = None
        self.group = None
        self.attenuation = None
        self.characteristics = [ ]

        self.metrics = { }

    def self.getid( self ):
        return( self.id )

    def self.getpos( self ):
        return( self.id )

    def self.getgrp( self ):
        return( self.id )

    def self.getatt( self ):
        return( self.id )

    def self.getchar( self ):
        return( self.id )

    def setAttributes( self, ID, Attrib ):
        """
        Assigns the attributes from the json file to the rsrc
        """
        self.id = ID
        self.position, self.group, self.attenuation, \
            self.characteristics = Attrib

class setup( object ):
    """
    Provides methods for reading a json file and creating lists 
    of tasks and resources objects
    """
    def __init__( self ):
        object.__init__( self )

        self.tasks = [ ]
        self.resources = [ ]

        self.slots = 1

    def setRsrcMetrics( self ):
        """
        Given a task, create a list with the distance metrics
        """
        for rsrc in self.getRsrcs( ):
            if type( rsrc.getpos( )[0] ) = type( "a" ):
                for task in self.getTasks( ):
                    if capable( task, rsrc ):
                        self.dynamic( task, rsrc )
            else:
                for task in self.getTasks( ):
                    if capable( task, rsrc ):
                        self.static( task, rsrc )

    def setTaskRsrc( self, fileName = "TaskRsrc.json" ):
        """
        Read the tasks and resources from a json file
        """
        fp = open( fileName )
        datajs = load( fp )
        for idx in datajs[ "Task" ]:
            tmpTask = task( )
            tmpTask.setAttributes( idx, datajs["Task"][idx] )
            self.tasks.append( tmpTask )
        for idx in datajs[ "Resource" ]:
            tmpRsrc = rsrc( )
            tmpRsrc.setAttributes( idx, datajs["Resource"][idx] )
            self.resources.append( tmpRsrc )

    def getTasks( self ):
        return( self.tasks )

    def getRsrcs( self ):
        return( self.resources )

    def getSlots( self ):
        return( self.slots )

    def setSlots( self, num ):
        maxSlots = 100000
        if type( num ) == type( 1 ):
            if 0 < num <= maxSlots:
                self.slots = num
        return( num )

    def capable( self, task, rsrc ):
        """        
        Determine if the task and resource are compatible
        """        
        rC = rsrc.getchar( )
        for tC in task.getchar( ):
            if tC in rC:
                continue
            else:
                return( False )
        return( True )

    def static( self, task, rsrc ):
        """
        Used for resources and tasks where both have fixed positions
        """
        tx, ty = task.getloc( )
        rx, ry = rsrc.getpos( )
        dx, dy = tx - rx, ty - ry
        dist = sqrt( dx * dx + dy * dy )
        mn, nm, mx = task.getdist( )
        fix = 1.1 * mx
        func = [ [ 0, 0.0 ], [ mn, 1.0 ], [ nm, 0.85 ], [ mx, 0.7 ], [ fix, 0.0 ] ]
        metric = round( self.PWL( dist, func), 5 )
        rsrc.metics[task.getid( )] = [ metric ] * self.getSlots( )

    def dynamic( self, task, rsrc ):
        """
        Used when the resource has a dynamic position and the task has a fixed position
        """
        dxeqn, dyeqn = rsrc.getpos( )
        tx, ty = task.getloc( )
        mn, nm, mx = task.getdist( )
        fix = 1.1 * mx
        rsrc.metrics[task.getid( )] = [ ]
        for s in range( self.getSlots( ) ):
            dx = tx - eval( dxeqn )
            dy = ty - eval( dyeqn )
            dist = sqrt( dx * dx + dy * dy )
            func = [ [ 0, 0.0 ], [ mn, 1.0 ], [ nm, 0.85 ], [ mx, 0.7 ], [ fix, 0.0 ] ]
            metric = round( self.PWL( dist, func), 5 )
            rsrc.metics[task.getid( )].append( metric )

    def PWL( self, entry, func ):
        """
        Return a value based on a piecewise-linear model.
        """
        result = 0.0
        if   entry <= func[0][0]:
            return( func[0][1] )
        elif entry > func[-1][0]:
            return( func[-1][1] )
        for idx in range( 0, len( func ) ):
            if entry > func[idx][0]:
                continue
            else:
                result = function[idx-1][1] + \
                            ( function[idx][1] - function[idx-1][1] ) * \
                            ( entry - func[idx-1][0] ) / ( func[idx][0] - func[idx-1][0] )
                return( result )

                    
