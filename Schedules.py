#!python
"""
  Various functions on a set of tasks and resources
"""
from random import shuffle

class sched( object ):
    """
    Places tasks on resources
    To be considered, the task and resource must have compatible 
    characteristics
    A schedule event (se) has the form
        [ start slot, stop slot, task ID ]
    """

    def __init__( self, tasks, rsrcs, schedule ):
        """
        """
        object.__init__( self )
        
        self.taskObjects = tasks
        self.resourceObjects = rsrcs
        self.scheduleDict = schedule

        self.theAttr = ""

    def gettos( self ):
        return( self.taskObjects )

    def getros( self ):
        return( self.resourceObjects )

    def getscd( self ):
        return( self.scheduleDict )

    def sortTasks( self, attribute, rev = 0 ):
        """
        """
        if attribute == "rand":
            tol = self.gettos( )
            shuffle( tol )
        else:
            tol = self.sortTaskObj( self.gettos( ), attribute, rev )
        return( tol )

    def sortRsrcs( self, attribute, rev = 0 ):
        """
        """
        if attribute == "rand":
            rol = self.getros( )
            shuffle( rol )
        else:
            rol = self.sortRsrcObj( self.getros( ), attribute, rev )
        return( rol )

    def map01( self, tattr, rattr, lim ):
        """
        Going through the resources in order, find the first available
        opportunity that meets:
          * compatible task and resource characteristics
          * metrics meet or exceed threshold
          * sufficient span for the style
        """
        tol = self.sortTasks( tattr )
        rol = self.sortRsrcs( rattr )

        reach = [ 0, 49 ]

        for tt in tol:
            if lim in [ 'min', 'nom', 'max' ]:
                span = tt.getspan( )[ [ 'min', 'nom', 'max' ].index( lim )]
            else:
                print( "WARN: Unable to get span using %s. Defaulting to 1" % lim )
                span = 1
            thresh = tt.getthr( )
            for rr in rol:
                if tt.getid( ) in rr.getmet( ).keys( ):
                    mets = tt.getmet( )[tt.getid( )]
                else:
                    print( "INFO: %s and %s are incompatible. No metrics" % \
                           ( tt.getid( ), rr.getid( ) ) )
                    continue
            oppInfo = [ -1, -1, 0 ]
            opps = self.findOpp( mets, thresh, reach, oppInfo )
            print( "INFO: %s %s: %s" % ( gg.getid( ), rr.getid( ), opps ) )

    def findOpp( self, mets, thresh, reach, oppInfo ):
        """
        mets are the distance metrics for the task on the resource
        oppInfo is: start slot, stop slot, length
        """
        flag = false
        opps = [ ]
        start, stop, length = oppInfo
        begin, end = reach
        for idx in range( begin, end + 1 ):
            if not flag:
                if  mets[idx] < thresh:
                    continue
                else:  ##  mets[idx] >= thresh
                    flag = true
                    oppInfo[0] = idx
                    oppInfo[2] = 1
            else:  ##  flag == True
                if mets[idx] < thresh:
                    flag = false
                    oppInfo[1] = idx
                    opps.append( oppInfo )
                    oppInfo = [ -1, -1, 0 ]
                else:  ##  mets[idx] >= thresh
                    oppInfo[2] += 1
            if idx == end:
                oppInfo[1] = idx
                opps.append( oppInfo )
        return( opps )

    def getReach( self, sch, init ):
        """
        Finds an open area on a resource starting at init
        Takes into account other se on the schedule, but not metrics
        """
        begin, end = [ init + 1, reach[1] ]
        if not sch:  ##  There is nothing currently on the schedule
            begin, end = ( 0, 49 )
        else:
            for se in sch:
                begin, end = ( init + 1, 49 )
        return( [ begin, end ] )

    def sortRsrcObj( self, objs, attrib, rev = 0 ):
        """
        Sort objects based on an attribute
        """
        if attrib in [ 'id', 'pos', 'grp', 'char' ]:
            self.theAttr = "get%s" % attrib
        
        objs = self.mysort( objs, attrib, rev = 0 )
        return( objs )

    def sortTaskObj
        if attrib in [ 'id', 'loc', 'imp', 'span', 'dist', 'char' ]:
            self.theAttr = "get%s" % attrib

        objs = self.mysort( objs, attrib, rev = 0 )
        return( objs )

    def cmpObj( self, obj1, obj2 ):
        val1 = eval( "obj1.%s( )" % self.theAttr )
        val2 = eval( "obj2.%s( )" % self.theAttr )
        if   val1 <  val2: return( -1 )
        elif val1 == val2: return(  0 )
        elif val1 >  val2: return(  1 )
        else: print( "ERR: problem with %s and %s comparison" % ( obj1, obj2 ) )

    def mysort( self, objs, attrib, rev = 0 ):
        """
        Sort objects based on an attribute.
        Uses inset sort - for when list.sort( ) doesn't take a cmp function
        """
        result = [ ]
        if attrib in [ 'id', 'loc', 'imp', 'span', 'dist', 'char', 'pos', 'grp' ]:
            self.theAttr = "get%s" % attrib
        
        for obj1 in objs:
            if not result: result = [ obj1 ]
            val1 = eval( "obj1.%s( )" % theAttr )
            if type( val1 ) == type( [ 1 ] ):
                val1 = val1[0]
            for idx in range( len( result ) ):
                val2 = eval( "obj1.%s( )" % theAttr )
                if type( val2 ) == type( [ 1 ] ):
                    val2 = val2[0]
                if val1 > val2:
                    result.insert( idx, obj1 )
                    break
                elif idx == len( result ) - 1:
                    result.append( obj1 )
                else:
                    continue
        return( result )
        
