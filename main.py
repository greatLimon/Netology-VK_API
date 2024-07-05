from App import App



def main():
    app = App()
    try:
        app.start()
    except:
        print('It seems something goes wrong!')
        app.bug()

if __name__ == '__main__':
    main()
 