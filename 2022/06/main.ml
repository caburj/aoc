open Base
open Stdio

let ( >> ) g f x = f (g x)

let find_marker len str =
  let checker = String.to_list >> Set.of_list (module Char) >> Set.length >> ( = ) len in
  String.fold_until
    ~init:0
    ~f:(fun i _ ->
      if checker (String.sub str ~pos:i ~len) then Stop (i + len) else Continue (i + 1))
    ~finish:(fun x -> x + len)
    str
;;

let () =
  let input_str = In_channel.input_all In_channel.stdin in
  printf "\nPart 1: %d\n" (find_marker 4 input_str);
  printf "Part 2: %d\n" (find_marker 14 input_str)
;;

(* cat input.txt | dune exec ./main.exe *)
