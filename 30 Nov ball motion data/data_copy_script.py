import pickle as pkl

names = ["field_recording", "field_recording_0", "field_recording_1", "field_recording_bouncing_0", "field_recording_bouncing_1", "field_recording_slower_0", "field_recording_slower_1"]

for filename in names:
    data = pkl.load(open(filename + ".pkl"))
    f = open(filename + ".txt", "w")
    f.writelines([str(i)+"\n" for i in data])
    f.close()
