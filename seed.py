from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# dummy users
ken = User(
    first_name="Ken",
    last_name="Yu",
    image_url="https://scontent-lga3-1.xx.fbcdn.net/v/t1.6435-9/41353875_238097000189493_5943158895600992256_n.jpg?stp=cp0_dst-jpg_e15_p320x320_q65&_nc_cat=104&ccb=1-7&_nc_sid=85a577&_nc_ohc=86V_N6hIqsgAX_375Mx&_nc_ht=scontent-lga3-1.xx&oh=00_AfAz3pYHyM2VZBKZVknRA8l4gFZpaHV2TEbLwy5cisbDmQ&oe=63B877D9",
)
chuck = User(
    first_name="Chuck",
    last_name="Webster",
    image_url="https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/chuck-webster/67de5562-9971-4322-b02d-0228eaa024c6-2ADA1119-40DF-4080-8626-A4BC2F9E/be31165905075f284399d4aaeb14f50c.jpeg",
)
elie = User(
    first_name="Elie",
    last_name="Schoppik",
    image_url="https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/elie/987a67e3-0ded-40da-858f-aba461253213-slack/34514a4259a5c332e659fb0f251da6a7.jpeg",
)
