import pandas as pd
import random

data = []

for _ in range(200):

    cgpa = round(random.uniform(5.0, 10.0), 2)
    aptitude = random.randint(40, 100)
    communication = random.randint(40, 100)
    coding = random.randint(35, 100)
    projects = random.randint(0, 5)
    internships = random.randint(0, 3)
    backlogs = random.randint(0, 5)

    score = (
        cgpa * 10
        + aptitude * 0.20
        + communication * 0.15
        + coding * 0.25
        + projects * 5
        + internships * 8
        - backlogs * 10
    )

    placed = 1 if score >= 115 else 0

    data.append([
        cgpa,
        aptitude,
        communication,
        coding,
        projects,
        internships,
        backlogs,
        placed
    ])

df = pd.DataFrame(
    data,
    columns=[
        "cgpa",
        "aptitude",
        "communication",
        "coding",
        "projects",
        "internships",
        "backlogs",
        "placed"
    ]
)

df.to_csv("dataset/placement_data.csv", index=False)

print("Dataset generated successfully!")