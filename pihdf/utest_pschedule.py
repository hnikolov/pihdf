import pschedule as s


# -- Testing the schedule conditions generators --
def set_stimuli():
    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]
    return stim_rx_1, stim_rx_2

def check_test_results( sname ):
#    s.default_scheduler.determine_schedule()
#    c    = s.default_scheduler.configs[i].condition_generator()
#    cond = s.default_scheduler.configs[i].cond_list
    c    = s.get_condition_generator(sname)
    cond = s.get(sname)
    
    
    for g, c in zip(c, cond):
        assert g == c, "Generator schedule condition != condition list"

# -----------------------------------------------
    
def utest_generator_t002():
    print "Test schedule type 2..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.clear_schedules()
    s.drive(stim_rx_2).after_every(stim_rx_1) # test_002
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")
    
def utest_generator_t003():
    print "Test schedule type 3..."
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.drive(stim_rx_2).after_every(stim_rx_1).start_at(3) # test_003
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t004():
    print "Test schedule type 4..."
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.drive(stim_rx_2).after(stim_rx_1).start_at(5) # test_004 (Enable after 5)
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t005():
    print "Test schedule type 5..."
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.drive(stim_rx_2).after_every(stim_rx_1).stimuli(3) # test_005
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t006():
    print "Test schedule type 6..."
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0) # test_006 (1st sample after reset)
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t007():
    print "Test schedule type 7..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    s.drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3) # test_007
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t008():
    print "Test schedule type 8..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    s.drive(stim_rx_2).after(stim_rx_1).samples([3, 7, 8]) # test_008 (1 after 3, 2 after 7, 3 after 8)
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_t009():
    print "Test schedule type 9..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    s.drive(stim_rx_2).samples([2, 4, 7]).after(stim_rx_1).samples([1, 4, 8]) # test_009 (2 after 1, 4 after 4, 7 after 8)
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")

def utest_generator_with_gaps():
    print "Test schedule type with gaps (not supported yet)..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    s.drive(stim_rx_2).with_gaps(4)
    assert len(s.default_scheduler.configs) == 1, "Extected 1 schedule configuration only"  
    check_test_results("rx_2")
    
def utest_generator_pink_ponk():
    print "Test schedule type ping_pong..."
    stim_rx_1, stim_rx_2 = set_stimuli()
    s.clear_configurations()
    s.default_scheduler.clear_schedules()
    s.drive(stim_rx_2).after_every(stim_rx_1).start_at(0) # start_at(0) == drive first sample after reset w/o condition
    s.drive(stim_rx_1).after_every(stim_rx_2)
    assert len(s.default_scheduler.configs) == 2, "Extected 2 schedule configurations"  
    check_test_results("rx_1")
    check_test_results("rx_2")

# -----------------------------------------------

# Some usage examples, tests
if __name__ == '__main__':

    utest_generator_t002()
    utest_generator_t003()
    utest_generator_t004()
    utest_generator_t005()
    utest_generator_t006()
    utest_generator_t007()
    utest_generator_t008()
    utest_generator_t009()
#    utest_generator_with_gaps() # Not supported
    utest_generator_pink_ponk()
    print "OK"
    
