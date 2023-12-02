open Base
open Stdio

let ( >> ) g f x = f (g x)

let to_pairs = function
  | [ a; b ] -> a, b
  | _ -> failwith "not gonna happen"
;;

let split = String.split ~on:' ' >> to_pairs

(* X -> play rock, Y -> play paper, Z -> play scissors *)
let process_with_strat_1 =
  split
  >> function
  | "A", "X" -> 1 + 3
  | "A", "Y" -> 2 + 6
  | "A", "Z" -> 3 + 0
  | "B", "X" -> 1 + 0
  | "B", "Y" -> 2 + 3
  | "B", "Z" -> 3 + 6
  | "C", "X" -> 1 + 6
  | "C", "Y" -> 2 + 0
  | "C", "Z" -> 3 + 3
  | _ -> failwith "should not happen"
;;

(* X -> lose the round, Y -> draw the round, Z -> win the round *)
let process_with_strat_2 =
  split
  >> function
  | "A", "X" -> 3 + 0
  | "A", "Y" -> 1 + 3
  | "A", "Z" -> 2 + 6
  | "B", "X" -> 1 + 0
  | "B", "Y" -> 2 + 3
  | "B", "Z" -> 3 + 6
  | "C", "X" -> 2 + 0
  | "C", "Y" -> 3 + 3
  | "C", "Z" -> 1 + 6
  | _ -> failwith "should not happen"
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  let () =
    List.fold lines ~init:0 ~f:(fun acc line -> acc + process_with_strat_1 line)
    |> printf "\npart 1: %d\n"
  in
  List.fold lines ~init:0 ~f:(fun acc line -> acc + process_with_strat_2 line)
  |> printf "part 2: %d\n"
;;
