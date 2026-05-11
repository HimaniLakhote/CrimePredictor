import pandas as pd
import random

locations = ['urban', 'rural']
times = ['day', 'night']
crime_levels = ['low', 'medium', 'high']
weapons = ['knife', 'gun', 'none']
motives = ['revenge', 'robbery', 'personal']
yes_no = ['yes', 'no']
suspects = ['a', 'b', 'c']

data = []

for _ in range(10000):
    location = random.choice(locations)
    time = random.choice(times)
    prev_crime = random.choice(crime_levels)
    weapon = random.choice(weapons)
    motive = random.choice(motives)
    fingerprints = random.choice(yes_no)
    witness = random.choice(yes_no)

    # 🔥 STRONG CRIME LOGIC
    if location == 'urban' and time == 'night' and prev_crime == 'high':
        crime = 'yes'
    elif prev_crime == 'low':
        crime = 'no'
    elif weapon != 'none':
        crime = 'yes'
    else:
        crime = random.choice(['yes', 'no'])

    # 🔥 STRONG SUSPECT LOGIC
    if weapon == 'knife' and motive == 'revenge':
        suspect = 'a'
    elif weapon == 'gun' and witness == 'yes':
        suspect = 'b'
    elif fingerprints == 'yes':
        suspect = 'c'
    else:
        suspect = random.choice(suspects)

    data.append([
        location, time, prev_crime, weapon, motive,
        fingerprints, witness, crime, suspect
    ])

df = pd.DataFrame(data, columns=[
    'location','time','previous_crime','weapon','motive',
    'fingerprints','witness','crime','suspect'
])

df.to_csv("crime_dataset.csv", index=False)

print("Dataset generated successfully ✅")