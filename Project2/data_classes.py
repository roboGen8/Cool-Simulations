class Stoplight(object):

    def __init__(self, e, w, n, s):
        self.e = e;
        self.w = w;
        self.n = n;
        self.s = s;


class Vehicle(object):

    def __init__(self, row):
        self.vehicle_ID = row[0]
        self.Frame_ID = []
        self.Tot_Frame = row[2]
        self.Epoch_ms = []
        self.Local_X = []
        self.Local_Y = []
        self.Global_X = []
        self.Global_Y = []
        self.Veh_Len = row[8]
        self.Veh_Wid = row[9]
        self.Veh_Class = row[10]
        self.Veh_Velocity = []
        self.Lane_ID = []
        self.Org_Zone = []
        self.Dest_Zone = []
        self.Intersection = []
        self.Section = []
        self.Direction = []
        self.Movement = []
        self.Preceding_Veh = []
        self.Following_Veh = []
        self.Spacing = []
        self.Headway = []

    def update(self, row):
        # self.vehicle_ID = row[0]
        self.Frame_ID.append(row[1])
        # self.Tot_Frame = row[2]
        self.Epoch_ms.append(row[3])
        self.Local_X.append(row[4])
        self.Local_Y.append(row[5])
        self.Global_X.append(row[6])
        self.Global_Y.append(row[7])
        # self.Veh_Len = row[8]
        # self.Veh_Wid = row[9]
        # self.Veh_Class = row[10]
        self.Veh_Velocity.append(row[11])
        self.Lane_ID.append(row[12])
        self.Org_Zone.append(row[13])
        self.Dest_Zone.append(row[14])
        self.Intersection.append(row[15])
        self.Section.append(row[16])
        self.Direction.append(row[17])
        self.Movement.append(row[18])
        self.Preceding_Veh.append(row[19])
        self.Following_Veh.append(row[20])
        self.Spacing.append(row[21])
        self.Headway.append(row[22])
