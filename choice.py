import random
import hard
import cv2

# Define the choices
bot = hard.RPSBot()

def comp_choice(scale):
    comp_choice = random.randint(1,3)
    img = cv2.imread(f"resources/{str(comp_choice)}.png", cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (scale*100, scale*100))
    return comp_choice, img

def hard_comp_choice(scale):
    comp_choice = int(bot.play())
    img = cv2.imread(f"resources/{str(comp_choice)}.png", cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (scale*100, scale*100))
    return comp_choice, img, len(bot.history)

def update_plan(move):
    bot.update(str(move))

def main():
    choice, img = comp_choice(5)
    cv2.imshow(str(choice), img)
    cv2.waitKey(0)
if __name__ == "__main__":
    main()