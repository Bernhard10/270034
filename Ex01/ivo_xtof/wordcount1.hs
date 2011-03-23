{--
  Last changed Time-stamp: <2009-03-17 20:36:16 xtof>
  $Id$

  Example provided by Christian Hoener zu Siederdissen

  buid: ghc --make wordcount1.hs
  run:  wordcount1 < FOO.txt
--}

module Main where

import Data.List
import qualified Data.ByteString as B
import qualified Data.ByteString.Char8 as C
import qualified Data.Map as M

main = do
  cnts <- B.getContents
  putStrLn $ show $ M.toList
           $ foldl' (\m k -> M.insertWith (+) k 1 m) M.empty
           $ C.words cnts

-- End of file
