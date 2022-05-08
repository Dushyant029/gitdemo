class State:
    _n=0
    _count=0+_n
    graph=[]

    def __init__(self):
        self.rules = []
        self._i = State._count
        self.hasreduce=0
        State._count = State._count+1
    
    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)
            if rule._closure==-1:
                self.hasreduce=1
    
    def goto(self, distination_index, symbol):
        
        g = [self._i, distination_index, symbol]
        if g not in State.graph:
            State.graph.append(g)
    
    def closure(self):
        for rule in self.rules:
            if rule.visited:
                continue
            for r in rule.visit():
                if r not in self.rules:
                    self.add_rule(r)

    def __eq__(self, s):
        "If self rules in s rules"
        if not isinstance(s, State):
            return NotImplemented
        eq = True
        if self.rules.__len__() > s.rules.__len__():
            return False
        for r in self.rules:
            eq = eq and (r in s.rules)
        return eq

    def __str__(self):
        s = []
        max_len=1
        for r in self.rules:
            line='    ['+str(r)
            s.append(line)
            if len(line) > max_len: max_len=len(line)
        for i in range(len(s)):
            pad = max_len-len(s[i])
            s[i]=s[i]+' '*pad+']'
        s.insert(0,''.join(['I',str(self._i),':',' '*(max_len-2)]))        
        return '\n'.join(s)

class Rule:
    _n=0
    augmented = []
    def __init__(self, lhs, rhs=[], dot_index=0):
        self.lhs = lhs
        if rhs == ['!εpslon']:
            self.rhs=[]
        else:
            self.rhs = rhs
        self._closure = dot_index
        
        if self.dotatend():
            self._closure = -1
        
        self.visited = 0

    def __str__(self):
        rhs = list(self.rhs)
        dot = self._closure
        if dot == -1:
            dot = len(rhs)
        rhs.insert(dot, '•')
        return self.lhs + ' → ' + ' '.join(rhs)

    def __eq__(self, rule):
        if not isinstance(rule, Rule):
            return NotImplemented
        return self.lhs == rule.lhs and self.rhs == rule.rhs and self._closure == rule._closure

    def handle(self):
        return self.rhs[self._closure]

    def visit(self):
        self.visited = 1
        if self._closure != -1:
            handle =  self.rhs[self._closure]
            if handle.startswith('`'):
                return [r.copy() for r in Rule.augmented if r.lhs == handle]
        return []
        
    def dotatend(self):
        if self._closure == len(self.rhs):
            return True
        return False

    def movedot(self):
        if self._closure == -1:
            return None
        return Rule(self.lhs, self.rhs, self._closure + 1)
    
    def copy(self):
        return Rule(self.lhs,self.rhs)