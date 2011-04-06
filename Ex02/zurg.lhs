
\section{Escape From Zurg: The Original}

\begin{code}
module Orig where

import Data.List

type Space m s = [([m],s)]

class SearchProblem s m where
  trans :: s -> [(m,s)]
  isSolution :: ([m],s) -> Bool
  space, solutions :: s -> Space m s

  space s = step ++ expand step where
    step = [ ([m],t) | (m,t) <- trans s ]
    expand ss = [ (ms++ns,t) | (ms,s) <- ss,
                               (ns,t) <- space s ]

  solutions = filter isSolution . space
\end{code}

\begin{code}
data Toy = Buzz | Hamm | Rex | Woody
  deriving (Eq,Ord,Show)
data Pos = L | R
  deriving (Eq,Show)

type Group = [Toy]
type BridgePos = (Pos,Group)
type Move = Either Toy Group

toys :: [Toy]
toys = [Buzz,Hamm,Rex,Woody]

time :: Toy -> Int
time Buzz = 5
time Woody = 10
time Rex = 20
time Hamm = 25

duration :: [Move] -> Int
duration = sum . map (either time (maximum . map time))

backw :: Group -> [(Move,BridgePos)]
backw xs = [(Left x, (L,sort (x:(toys \\ xs)))) | x <- xs]

forw :: Group -> [(Move,BridgePos)]
forw xs = [(Right [x,y], (R, delete y ys))
          | x <- xs, let ys = delete x xs, y <- ys, x < y]

instance SearchProblem BridgePos Move where
  trans (L,l) = forw l
  trans (R,l) = backw (toys \\ l)
  isSolution (ms,s) = s == (R,[]) && duration ms <= 60

solution :: Space Move BridgePos
solution = solutions (L,toys)

\end{code}

