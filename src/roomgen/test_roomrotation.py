'''
Simple script to test the logic for computing roomtype rotations.
'''
from room import *

def test():
    # Each element is a test.
    # Each element is a tuple of the form:
    # north, east, south, west, expected room type, expected rotation
    # 1 means True, 0 means False
    # This is an exhaustive list of all possible room configurations.
    test_entries = [
    (0, 0, 0, 1, RoomType.north, Rotation.clockwise270),
    (0, 0, 1, 0, RoomType.north, Rotation.clockwise180),
    (0, 0, 1, 1, RoomType.north_east, Rotation.clockwise180),
    (0, 1, 0, 0, RoomType.north, Rotation.clockwise90),
    (0, 1, 0, 1, RoomType.north_south, Rotation.clockwise90),
    (0, 1, 1, 0, RoomType.north_east, Rotation.clockwise90),
    (0, 1, 1, 1, RoomType.north_east_south, Rotation.clockwise90),
    (1, 0, 0, 0, RoomType.north, Rotation.clockwise0),
    (1, 0, 0, 1, RoomType.north_east, Rotation.clockwise270),
    (1, 0, 1, 0, RoomType.north_south, Rotation.clockwise0),
    (1, 0, 1, 1, RoomType.north_east_south, Rotation.clockwise180),
    (1, 1, 0, 0, RoomType.north_east, Rotation.clockwise0),
    (1, 1, 0, 1, RoomType.north_east_south, Rotation.clockwise270),
    (1, 1, 1, 0, RoomType.north_east_south, Rotation.clockwise0),
    (1, 1, 1, 1, RoomType.north_east_south_west, Rotation.clockwise0),
    ]
    for test_entry in test_entries:
        (north, east, south, west, expected_room_type, expected_rotation) = test_entry

        # Convert the 0s and 1s to True's and False's
        def to_bool(num):
            if num == 1:
                return True
            else:
                return False
        (north, east, south, west) = [to_bool(t) for t in (north, east, south, west)]

        # Determine the actual room type and rotation.
        (actual_room_type, actual_rotation) = compute_rotated_room(north, east, south, west)

        # Check if the result is correct.
        if expected_rotation != actual_rotation or expected_room_type != actual_room_type:
            print "Failed on (%s, %s, %s, %s)" % (north, east, south, west)
            print "Expected type=%d, rotation=%d" % (expected_room_type, expected_rotation)
            print "Actual type=%d, rotation=%d" % (actual_room_type, actual_rotation)
            exit(1)

if __name__=="__main__":
    test()
