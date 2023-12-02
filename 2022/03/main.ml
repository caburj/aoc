open Stdio
open Base

(* Part 1 solution. Cut each line into half, create set of
   characters for each half, take the intersection, convert to
   equivalent value, take the sum. *)

let ( >> ) g f x = f (g x)
let sum = List.fold ~f:( + ) ~init:0

let split line =
  let n = String.length line in
  let h = n / 2 in
  String.sub line ~pos:0 ~len:h, String.sub line ~pos:h ~len:h
;;

let make_char_set = String.to_list >> Set.of_list (module Char)

let get_priority c =
  let v = Char.to_int c in
  if v >= 65 && v <= 90
  then v - 64 + 26 (* capital letters, A -> 65, +26 because capital *)
  else v - 96 (* small letter, a -> 97 *)
;;

let search_issue (first, second) =
  let fset = make_char_set first in
  let sset = make_char_set second in
  Set.inter fset sset |> (Fn.flip Set.nth) 0 |> Option.value ~default:' '
;;

(* Part 2. *)

let find_common (first, second, third) =
  let fset = make_char_set first in
  let sset = make_char_set second in
  let tset = make_char_set third in
  Set.inter fset sset
  |> Set.inter tset
  |> (Fn.flip Set.nth) 0
  |> Option.value ~default:' '
;;

let rec group_by_3 = function
  | [] -> []
  | a :: b :: c :: tl -> (a, b, c) :: group_by_3 tl
  | _ -> failwith "not gonna happen"
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  let () =
    lines
    |> List.map ~f:(split >> search_issue >> get_priority)
    |> sum
    |> printf "\nPart 1: %d\n"
  in
  let () =
    lines
    |> group_by_3
    |> List.map ~f:(find_common >> get_priority)
    |> sum
    |> printf "Part 2: %d\n"
  in
  ()
;;
