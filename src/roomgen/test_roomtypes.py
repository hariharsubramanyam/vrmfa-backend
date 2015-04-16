'''
Simple script to test the logic for computing roomtype rotations.
'''
import roomtypes

def test():
    # Each element is a test.
    # Each element is a tuple of the form:
    # north, east, south, west, expected room type, expected rotation
    test_entries = [
    (True, True, False, False, roomtypes.RoomType.north_east, roomtypes.Rotation.clockwise0), # Adjacent rooms no rotation.
    (True, False, True, True, roomtypes.RoomType.north_east_south, roomtypes.Rotation.clockwise180), # Three rooms.
    (False, True, False, True, roomtypes.RoomType.north_south, roomtypes.Rotation.clockwise90), # Opposite rooms with rotatio with rotation.
    (True, False, False, False, roomtypes.RoomType.north, roomtypes.Rotation.clockwise0), # Single rooom no rotation.
    (True, True, True, True, roomtypes.RoomType.north_east_south_west, roomtypes.Rotation.clockwise0) # Four rooms.
    ]

    for test_entry in test_entries:
        (north, east, south, west, expected_room_type, expected_rotation) = test_entry
        (actual_room_type, actual_rotation) = roomtypes.compute_rotated_room(north, east, south, west)
        if expected_rotation != actual_rotation or expected_room_type != actual_room_type:
            print "Failed on (%s, %s, %s, %s)" % (north, east, south, west)
            print "Expected type=%d, rotation=%d" % (expected_room_type, expected_rotation)
            print "Actual type=%d, rotation=%d" % (actual_room_type, actual_rotation)
            exit(1)

if __name__=="__main__":
    test()
