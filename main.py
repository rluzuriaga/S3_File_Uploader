from UI.ProgramController import ProgramController
from Database import Database

def main():
    with Database() as DB:
        DB.create_database()

    pc = ProgramController()
    pc.mainloop()

if __name__ == "__main__":
    main()
