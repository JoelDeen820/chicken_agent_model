from utilities.barn_enviroment import Barn
import matplotlib.pyplot as plt


def main(args=None):
    barn = Barn((300, 300), 500)
    barn.draw()
    plt.show()
    # for i in range(30):
    #     barn.step()


if __name__ == '__main__':
    main()
