from Clocks import TestClock
from TimeoutManager import TimeoutManager

def do_callback(name, callbacks_list):
    callbacks_list.append(name);
    print(f"Item {name}'s callback")

def test1():
    clock = TestClock()
    timeouts = TimeoutManager(clock)
    
    actual_callbacks = []
    
    # Test with items:
    # Added at clock time = 0:
    # - item D with delay 500 (callback time is 500)
    # - item A with delay 100 (callback time is 100)
    # Added at clock time = 50
    # - item B with delay 150 (callback time is 200)
    clock.set_time(0)
    timeouts.add_timeout(lambda: do_callback("D", actual_callbacks), 500)
    timeouts.add_timeout(lambda: do_callback("A", actual_callbacks), 100)
    clock.set_time(50)
    timeouts.add_timeout(lambda: do_callback("B", actual_callbacks), 150)
    
    # Do an update with clock time = 100, which should invoke item A's callback
    clock.set_time(100)
    print("Updating with clock time = 100. Item A should show below.")
    timeouts.update()
    
    # Verify that only item A's callback was called
    if not verify_callbacks(actual_callbacks, ["A"]):
        return False
    
    # Do another update with a clock time of 150, which shouldn't invoke any
    # callbacks
    clock.set_time(150)
    print("Updating with clock time = 150. No callbacks should show below.")
    timeouts.update()
    
    # Verify that still only item A's callback has been called
    if not verify_callbacks(actual_callbacks, ["A"]):
        return False
    
    # Add more timeouts at clock time = 300:
    # - item E with delay 500 (callback time is 800)
    # - item C with delay 100 (callback time is 400)
    clock.set_time(300)
    print("Adding timeouts E and C")
    timeouts.add_timeout(lambda: do_callback("E", actual_callbacks), 500)
    timeouts.add_timeout(lambda: do_callback("C", actual_callbacks), 100)
    
    # Verify that adding new timeouts didn't invoke any new callbacks
    if not verify_callbacks(actual_callbacks, ["A"]):
        return False
    
    # Do an update with a clock time of 350, which should invoke item B's
    # callback
    clock.set_time(350)
    print("Updating with clock time = 350. Item B should show below.")
    timeouts.update()
    
    # Verify callbacks: A and B called, others not
    if not verify_callbacks(actual_callbacks, ["A", "B"]):
        return False
    
    # Do an update with a clock time of 550, which should invoke item C's
    # callback and item D's callback, in that order
    clock.set_time(550)
    print("Updating with clock time = 550. Item C and D should show below, " +
        "in that order.")
    timeouts.update()
    
    # Verify callbacks: A, B, C, and D
    if not verify_callbacks(actual_callbacks, ["A","B","C","D"]):
        return False
    
    # Do another update with a clock time of 700, which shouldn't invoke any
    # callbacks
    clock.set_time(700)
    print("Updating with clock time = 700. No callbacks should show below.")
    timeouts.update()
   
    #  Verify callbacks: again just A, B, C, and D
    if not verify_callbacks(actual_callbacks, ["A", "B", "C", "D"]):
        return False
   
    # Do a final update with time = 900, which should invoke item E's callback
    clock.set_time(900)
    print("Updating with clock time = 900. Item E should show below.")
    timeouts.update()
   
    # Verify callbacks: A, B, C, D, and E
    if not verify_callbacks(actual_callbacks, ["A","B","C","D","E"]):
        return False
    
    return True

def test2():
    clock = TestClock()
    timeouts = TimeoutManager(clock)
    
    actual_callbacks = []
   
    # At t = 0:
    # - Add item A with delay 800 (callback time is 800)
    clock.set_time(0)
    print("At t=0, adding timeout A with delay = 800")
    timeouts.add_timeout(lambda: actual_callbacks.append("A"), 800)
   
    # At t = 50:
    # - Add item D with delay 600 (callback time is 650)
    clock.set_time(50)
    print("At t=50, adding timeout D with delay = 600")
    timeouts.add_timeout(lambda: actual_callbacks.append("D"), 600)
   
    # At t = 100:
    # - Add item C with delay 200 (callback time is 300)
    clock.set_time(100)
    print("At t=100, adding timeout C with delay = 200")
    timeouts.add_timeout(lambda: actual_callbacks.append("C"), 200)
   
    # At t = 150:
    # - Add item E with delay 250 (callback time is 400)
    clock.set_time(150)
    print("At t=150, adding timeout E with delay = 250")
    timeouts.add_timeout(lambda: actual_callbacks.append("E"), 250)
   
    # At t = 200:
    # - Add item B with delay 50 (callback time is 250)
    # - Update, then verify that no callback have yet been called
    clock.set_time(200)
    print("At t=200, adding timeout B with delay = 50, then " +
        "updating")
    timeouts.add_timeout(lambda: actual_callbacks.append("B"), 50)
    timeouts.update()
    if not verify_callbacks(actual_callbacks, []):
        return False
   
    # At t = 400:
    # - Update, then verify that callbacks B, C, and E have been called
    clock.set_time(400)
    print("At t=400, updating")
    timeouts.update()
    if not verify_callbacks(actual_callbacks, ["B", "C", "E"]):
        return False
   
    # At t = 450:
    # - Add item F with delay 100 (callback time is 550)
    clock.set_time(450)
    print("At t=450, adding timeout F with delay = 100")
    timeouts.add_timeout(lambda: actual_callbacks.append("F"), 100)
   
    # At t = 600:
    # - Update, then verify callbacks: B and C from earlier, E and F now
    clock.set_time(600)
    print("At t=600, updating")
    timeouts.update()
    if not verify_callbacks(actual_callbacks, ["B", "C", "E", "F"]):
        return False
   
    # At t = 800:
    # - Update, then verify callbacks: B, C, E, F, D, A
    clock.set_time(800)
    print("At t=800, updating")
    timeouts.update()
    if not verify_callbacks(actual_callbacks, ["B", "C", "E", "F", "D", "A"]):
        return False
    
    return True

def verify_callbacks(actual, expected):
    # Compare list lengths first
    are_equal = True
    if len(actual) == len(expected):
        i = 0
        while are_equal and i < len(actual):
            if actual[i] != expected[i]:
                are_equal = False
            i += 1
    else:
        are_equal = False
       
    # Print results
    print(("PASS" if are_equal else "FAIL") +
        ": Verification of invoked callbacks\n" +
        f"  Expected: {expected}\n" +
        f"  Actual:   {actual}")
    
    return are_equal

# Main program code follows

print("---- Test 1 ----")
test1_result = test1()
print("\n---- Test 2 ----")
test2_result = test2()

print()
print(f"Local test 1: {'PASS' if test1_result else 'FAIL'}")
print(f"Local test 2: {'PASS' if test2_result else 'FAIL'}")