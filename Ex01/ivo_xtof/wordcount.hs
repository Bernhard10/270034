{--
  Last changed Time-stamp: <2008-04-05 18:19:52 xtof>
  $Id$
  
  compile with: ghc -Wall --make wordcount.hs -o wordcount
  test with:    look foo | ./wordcount | less
  result:       ("footweary",2)
                ("footwall",2)
                ("footsore",2)
                ("footslog",2)
                ("footpound",2)
                ("footnote",2)
                ("footmark",2)
                ("footloose",2)
                ...
--}

module Main where

import Char
import Data.List
import qualified Data.Map
import Data.Ord

-- filters out all non-alphabetic from arg1 and canonizes remaining
-- characters to lower case
normalize :: [Char] -> [Char]
normalize = map toLower . filter isAlpha

-- splits given string at whitespace into a list of strings. each of
-- them is converted to a canonical form. strings canonizing to the
-- empty string are removed from the list.
nwords :: [Char] -> [[Char]]
nwords = filter (not . null) . map normalize . words

-- insert strings into a Data.Map incrementing the associated value
wordCount :: [Char] -> Data.Map.Map [Char] Int
wordCount w = foldr (uncurry (Data.Map.insertWith (+)))
	            Data.Map.empty
		    (zip (nwords w) [1,1 ..])

-- read text from stdin and print a frequency sorted list of the words
-- to stdout
main :: IO ()
main = do
       s <- getContents
       mapM_ print $ reverse . sortBy (comparing snd)
		   $ Data.Map.toList $ wordCount s

-- End of file
