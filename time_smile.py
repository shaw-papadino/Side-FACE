


str = ["111AB.CDE","111abc.def","kgjkjgoiajis.jpg"]

# for i in str:
#     slice = i[-6:-4]
#     print(slice)
i = "13"
m = "09"
sum = 0
time_smile = []
if m[0] == "0":
    m = m.replace("0","")
    #print(int(i) - int(m))
if int(i) - int(m) >= 3 and int(i) - int(m) <= 5:
    sum += int(i) - int(m)
    print(sum)
else:
    time_smile.append(sum)
