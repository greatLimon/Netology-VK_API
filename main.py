from App import App

def main():
    try:
        app = App()
        app.start()
        print('Done!')
    except TypeError:
        print('App is closed')
    except:
        print('It seems something goes wrong!')
        app.crush()

if __name__ == '__main__':
    main()
 