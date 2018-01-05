#!python
"""
  A game where the objective is to map tasks onto resources across
  spans of specific duration to maximize value. The scheduling
  problem.
"""
from TaskRsrc import task, rsrc, setup
from Schedules import sched

class mapping( object ):
    """
    Create a schedule (a mapping)
    Display a schedule
    Score a schedule 
      - self.schedule: a dictionary where the keys are the available 
        resources. A list is associated with each resource that has
        start and stop times for each task using that resource.
    """

    def __init__( self ):
        """
        """
        object.__init__( self )

        self.schedule = { }

        self.ee = setup( )
        self.ee.setSlots( 50 )
        self.ee.setTaskRsrc( )
        self.ee.setRsrcMetrics( )

        self.weights = {
            "slot" : "dmet * imp",
            "task" : "sum( slot )",
            "rsrc" : "sum( task ) * rsrcWt",
            "rsrcWt" : "something - not sure yet"
            }

    def create( self ):
        """
        The schedule is a dictionary with the resources as keys.
        For each resource, there is a list or schedule events (se)
        which includes the start and stop times and the task ID.
            [ start, stop, taskID ]
        The task and resource must be compatible
        The distance metric for all slots between start and stop
        must exceed the task's threshold.
        """
        for rsrc in self.ee.getRsrcs( ):
            self.schedule[rsrc.getid( )] = [ ]

    def getSched( self ):
        return self.schedule

    def doMap( self ):
        sc = sched( self.ee.getTasks( ), self.ee.getRsrcs( ), self.getSched( ) )
        self.schedule = sc.map01( 'id', 'id', 'min' )

    def display( self ):
        """
        display( key )
            0: do not show anything
            1: display the tasks
            2: display the resources
            3: display the tasks and resources
            4: display the tasks, resources and the distance metrics 
               on each resource
        """
        if style in [ 1, 3, 4 ]:
            print( "\nThe Tasks: " )
            for tt in mm.ee.getTasks( ):
                mn, nm, mx = tt.getdist( )
                print( "\t%s %s %s %s [ %5.3f, %5.3f, %5.3f ] %s" % \
                       ( tt.getid( ), tt.getloc( ), tt.getimp( ),
                         tt.getspan( ), mn, nm, mx, tt.getchar( ) ) )
        if style in [ 2, 3, 4 ]:
            print( "\nThe Resources: " )
            for rr in mm.ee.getRsrcs( ):
                print( "\t%s %s %s %s" % ( rr.getid( ), rr.getpos( ), rr.getchar( ) ) )
                if style in [ 4 ]:
                    print( "\nThe distance metrics:" )
                    for tt in rr.getmet( ):
                        print( "%s: " % tt )
                        for dm in rr.getmet( )[tt]:
                            print( "%5.3f" % dm ),
                    print( "\n" )

    def show( self, style = 1 ):
        """
        Show the schedule in various styles
            0: do not show the schedule
            1: show by resource
            2: show by importance
            3: show by computed value
        """
        if style == 1:
            print( "INFO: print the schedule in style %d" % style )
        elif style == 2:
            print( "INFO: print the schedule in style %d" % style )
        elif style == 3:
            print( "INFO: print the schedule in style %d" % style )
        else:
            print( "WARN: invalid print schedule style %s" % style )

    def score( self ):
        """
        Compute the value for a schedule mapping. The same scoring is 
        used for every schedule.
        """
        result = 0.0
        for rr in self.ee.getRsrcs( ):
            value = self.scoreRsrc( rr )
            result += value
        print( "INFO: Value for the schedule is %s " % ( rr, result ) )
        return( result )

    def scoreRsrc( self, rr ):
        """
        Compute the value of the schedule for a single resource
        """
        result = 0.0
        for tt in self.getSched( )[rr.getid( )]:
            for se in tt:
                result += 1
        print( "INFO: Value for %s: %s " % ( rr, result ) )
        return( result )
        
mm = mapping( )

ss = sched( mm.ee.getTasks( ), mm.ee.getRsrcs( ), mm.getSched( ) )
ss.map01( "id", "id", "min" )

mm.score( )

