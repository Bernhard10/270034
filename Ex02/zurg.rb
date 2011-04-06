# extend class Array by memberfunction each_pair
# hich returns a lol with all pairs
class Array
  def each_pair
    each_with_index do |x, i|
      self[i + 1 ... length].each {|y| yield [x, y]}
    end
  end
end

# Symbol#to_proc trick
# can be used to change the call
# result = names.map {|name| name.upcase}
# into the syntacticaly simpler call
# result = names.map{&:upcase}
# http://pragdave.pragprog.com/pragdave/2005/11/symbolto_proc.html
class Symbol
  def to_proc
    proc { |obj, *args| obj.send(self, *args) }
  end
end

# define structure SearchProblem to represent the search problem
SearchProblem = Struct.new(:initial) do
  def each_candidate(&proc)
    step [], initial, &proc
  end
  
  def step(history, state, &proc)
    if state.terminal?
      yield history
    else
      state.each_successor do |move, state|
        step history + [move], state, &proc
      end
    end
  end
end

# define structure Toy to reperesent the toys
Toy = Struct.new(:name, :time)
# define array of toys
Toys = [
  Toy.new(:hamm, 25),
  Toy.new(:buzz, 5),
  Toy.new(:rex, 20),
  Toy.new(:woody, 10)
]

# define structure Move to represent transitions between states
# member var direction = R|L
# member var who := (toy1, toy2) for R move
#            who := toy for L move
# member fun cost := returns time taken to complete the move\
#            cost uses the Symbol#to_proc trick
#            http://pragdave.pragprog.com/pragdave/2005/11/symbolto_proc.html
Move = Struct.new(:direction, :who) do
  def cost
#   who.collect{ |toy| toy.time }.max
#   using the Symbol Symbol#to_proc trick we get
    who.collect(&:time).max
  end
end

# define structure State
# member var pos   := represents current flashlight position
# member var group := representing toys on lhs of the bridge
#                     Toys - group are the toys on the rhs of the bridge
State = Struct.new(:pos, :group) do
  def terminal?
    group.empty?
  end
  
  def each_successor
    case pos
      when :left
        group.each_pair do |pair|
          yield Move.new(:right, pair), State.new(:right, group - pair)
        end
      when :right
        (Toys - group).each do |toy|
          yield Move.new(:left, [toy]), State.new(:left, group + [toy])
        end
    end
  end
end

# do the simulation
problem = SearchProblem.new State.new(:left, Toys)
puts problem.each_candidate {|history|
  break history if history.inject(0) {|acc, move| acc + move.cost} <= 60
}
