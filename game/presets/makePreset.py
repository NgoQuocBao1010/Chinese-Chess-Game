import os

DIR = os.path.dirname(__file__)
SEPERATOR = " ******** "


# with open(os.path.join(DIR, "standard.cfg"), "a") as f:
#     pieces = []
#     f.write(f"red{SEPERATOR}advisor{SEPERATOR}0, 1\n")

final = []
pieces = ["chariot", "horse", "elephant", "advisor"]

l1 = list(range(0, 4))
l2 = list(range(8, 4, -1))

for r, side, cannonR, solR in zip([0, 9], ("blue", "red"), [2, 7], [3, 6]):

    for piece, col in zip(pieces, l1):
        final.append([ piece, r, col, side ])
    
    final.append([ "lord", r, 4, side ])

    for piece, col in zip(pieces, l2):
        final.append([ piece, r, col, side ])
    
    for col in [1, 7]:
        final.append([ "cannon", cannonR, col, side ])
    
    for col in [0, 2, 4, 6, 8]:
        final.append([ "soldier", solR, col, side ])
    



with open(os.path.join(DIR, "standard.cfg"), "w") as f:
    for piece, row, col, side in final:
        f.write(f"{piece}{SEPERATOR}{row}{SEPERATOR}{col}{SEPERATOR}{side}\n")