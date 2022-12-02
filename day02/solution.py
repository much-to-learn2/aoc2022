class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"<Node: {self.val}>"

class RockPaperScissors:
    opponentChoice = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
    }

    playerChoice = {
        "X": "rock",
        "Y": "paper",
        "Z": "scissors",
    }

    def __init__(self):
        self.rock = Node(1)
        self.paper = Node(2, self.rock)
        self.scissors = Node(3, self.paper)
        self.rock.next = self.scissors

        # map code to the method we need to run to get our choice
        self.outcome = {
            "X": (self.get_loser, 0),
            "Y": (self.get_self, 3),
            "Z": (self.get_winner, 6), 
        }

    def get_winner(self, choice: str) -> Node:
        """
        who beats the selected choice?
        """
        return getattr(self, choice).next.next

    def get_self(self, choice: str) -> Node:
        """
        who ties the selected choice? 3Head
        """
        return getattr(self, choice)

    def get_loser(self, choice: str) -> Node:
        """
        who loses to the selected choice?
        """
        return getattr(self, choice).next

    def get_score1(self, oppCode: str, playerCode: str) -> int:
        """
        game score according to first ruleset
        """
        opp = self.opponentChoice[oppCode]
        player = self.playerChoice[playerCode]
    
        if self.get_winner(opp) == self.get_self(player):
            # player beats opp
            gameScore = 6
        elif opp == player:
            gameScore = 3
        elif self.get_loser(opp) == self.get_self(player):
            gameScore = 0
        
        choiceScore = self.get_self(player).val
        return choiceScore + gameScore
            
    def get_score2(self, oppCode: str, outcomeCode: str) -> int:
        """
        game score according to second ruleset
        """
        get_player_choice, gameScore = self.outcome[outcomeCode]
        opp = self.opponentChoice[oppCode]
        player = get_player_choice(opp)
        return gameScore + player.val 
        

with open("input.txt", "r") as f:
    rps = RockPaperScissors()
    solution1, solution2 = 0, 0
    for line in f.readlines():
        oppCode, playerCode = line.rstrip("\n").split(" ")
        solution1 += rps.get_score1(oppCode, playerCode)

        outcome = playerCode
        solution2 += rps.get_score2(oppCode, outcome)

print(f"{solution1=}")
print(f"{solution2=}")
