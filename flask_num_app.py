from flask import Flask, render_template, request, redirect, url_for
import random
import copy

app=Flask(__name__)

class app_game():
    def __init__(self,game_type):
        self.game_type=game_type
        self.box_make()
        

    #ボタンのランダム設置
    def box_make(self):
        self.randombox=[[],[],[],[],[],[]]
        self.numall=[]
        self.numall_copy=[]
        
        self.push_list=[]
        self.button_color=[[],[],[],[],[],[]]

        for i in range(6):
            for j in range(6):
                self.button_color[i].append("white")

        if self.game_type=="add":
            self.minbutton=1
        elif self.game_type=="mul":
            self.minbutton=2

        for i in range(6):
            for j in range(6):
                self.num=random.randint(self.minbutton,5)
                self.randombox[i].append(self.num)
                self.numall.append(self.num)
        
        self.numall_copy=copy.copy(self.numall)

        if self.game_type=="add":
            self.push_addmul=0
            self.add_target_num()
        elif self.game_type=="mul":
            self.push_addmul=1
            self.mul_target_num()
        

    #足し算のターゲットとなる数字の設置
    def add_target_num(self):
        self.targetnum=0
        if len(self.numall_copy)>=5:
            self.time=random.randint(1,4)
            for k in range(self.time):
                self.targetidx=random.randint(0,len(self.numall_copy)-1)
                self.targetnum+=self.numall_copy[self.targetidx]
                del self.numall_copy[self.targetidx]

        else:
            for k in self.numall_copy:
                self.targetnum+=k

    #掛け算のターゲットとなる数字の設置
    def mul_target_num(self):
        self.targetnum=1
        if len(self.numall_copy)>=5:
            self.time=random.randint(1,4)
            for k in range(self.time):
                self.targetidx=random.randint(0,len(self.numall_copy)-1)
                self.targetnum*=self.numall_copy[self.targetidx]
                del self.numall_copy[self.targetidx]

        else:
            for k in self.numall_copy:
                self.targetnum*=k

    #足し算の押したボタンの数字をリスト化
    def add_push_num(self,num,i,j):
        if self.button_color[i][j]=="white":
            self.push_addmul+=num
            self.push_list.append(num)
            self.button_color[i][j]="violent"

        elif self.button_color[i][j]=="violent":
            self.push_addmul-=num
            self.push_list.remove(num)
            self.button_color[i][j]="white"

        self.checktarget()

    #掛け算の押したボタンの数字をリスト化
    def mul_push_num(self,num,i,j):
        if self.button_color[i][j]=="white":
            self.push_addmul*=num
            self.push_list.append(num)
            self.button_color[i][j]="violent"

        elif self.button_color[i][j]=="violent":
            self.push_addmul/=num
            self.push_list.remove(num)
            self.button_color[i][j]="white"

        self.checktarget()




    def checktarget(self):
        if self.push_addmul==self.targetnum:
            for a in self.push_list:
                self.numall.remove(a)

            for a in range(6):
                for b in range(6):
                    if self.button_color[a][b]=="violent":
                        self.randombox[a][b]=""
            
            self.numall_copy=copy.copy(self.numall)
            self.push_list=[]

            
            if self.game_type=="add":
                self.push_addmul=0
                self.add_target_num()
            elif self.game_type=="mul":
                self.push_addmul=1
                self.mul_target_num()

        if len(self.numall)==0:
           self.game_clear=1



@app.route("/",methods=["GET","POST"])
def home():
    global game_judge
    game_judge=0
    return render_template("home.html")

@app.route("/game",methods=["GET","POST"])
def game():
    global Game, game_judge
    game_type=request.form.get("button")

    if game_judge==0:
        Game=app_game(game_type)
        Game.game_clear=0
        game_judge=1
        
    

    if request.method=="POST":
        num=request.form.get("num") 
        if num:
            pushnum, push_i, push_j = map(int, num.split(","))
            if Game.game_type=="add":
                Game.add_push_num(pushnum, push_i, push_j)
            elif Game.game_type=="mul":
                Game.mul_push_num(pushnum, push_i, push_j)
            
        
        if Game.game_clear==1:
            return redirect(url_for("clear"))

        
        return render_template("game.html",randombox=Game.randombox,target=Game.targetnum,button_color=Game.button_color)

    return render_template("game.html",randombox=Game.randombox,target=Game.targetnum,button_color=Game.button_color)


@app.route("/clear")
def clear():
    return render_template("clear.html")


if __name__=="__main__":
    game_judge=0
    Game=None
    app.run(debug=True)
