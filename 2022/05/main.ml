open Base
open Stdio

(* NOTE: I'm too lazy to parse the original input, so I just manually converted
   the 'stack' of crates into [int list array] of crates.
   Therefore, this solution can only work when given only the series of [moves].
   See [moves.txt].
   IMPROVEMENT: Maybe a pure functional solution?
   *)

let crates =
  [| [ ' ' ] (* dummy *)
   ; [ 'F'; 'L'; 'M'; 'W' ]
   ; [ 'F'; 'M'; 'V'; 'Z'; 'B' ]
   ; [ 'Q'; 'L'; 'S'; 'R'; 'V'; 'H' ]
   ; [ 'J'; 'T'; 'M'; 'P'; 'Q'; 'V'; 'S'; 'F' ]
   ; [ 'W'; 'S'; 'L' ]
   ; [ 'W'; 'J'; 'R'; 'M'; 'P'; 'V'; 'F' ]
   ; [ 'F'; 'R'; 'N'; 'P'; 'C'; 'Q'; 'J' ]
   ; [ 'B'; 'R'; 'W'; 'Z'; 'S'; 'P'; 'H'; 'V' ]
   ; [ 'W'; 'Z'; 'H'; 'G'; 'C'; 'J'; 'M'; 'B' ]
  |]
;;

let crates_dup =
  [| [ ' ' ] (* dummy *)
   ; [ 'F'; 'L'; 'M'; 'W' ]
   ; [ 'F'; 'M'; 'V'; 'Z'; 'B' ]
   ; [ 'Q'; 'L'; 'S'; 'R'; 'V'; 'H' ]
   ; [ 'J'; 'T'; 'M'; 'P'; 'Q'; 'V'; 'S'; 'F' ]
   ; [ 'W'; 'S'; 'L' ]
   ; [ 'W'; 'J'; 'R'; 'M'; 'P'; 'V'; 'F' ]
   ; [ 'F'; 'R'; 'N'; 'P'; 'C'; 'Q'; 'J' ]
   ; [ 'B'; 'R'; 'W'; 'Z'; 'S'; 'P'; 'H'; 'V' ]
   ; [ 'W'; 'Z'; 'H'; 'G'; 'C'; 'J'; 'M'; 'B' ]
  |]
;;

let ( >> ) g f x = f (g x)

let parse_move line =
  line
  |> (String.split ~on:' '
     >> function
     | [ _; a; _; b; _; c ] -> Int.of_string a, Int.of_string b, Int.of_string c
     | _ -> failwith "not gonna happen")
;;

(* Crane from part 1. I can only lift 1 crate at a time. *)
let move_9000 crates (count, src, dst) =
  for _ = 1 to count do
    let src_stack = crates.(src) in
    let dst_stack = crates.(dst) in
    match src_stack with
    | hd :: tl ->
      crates.(src) <- tl;
      crates.(dst) <- hd :: dst_stack
    | [] -> ()
  done
;;

(* Crane from part 2. It can lift multiple crates at a time. *)
let move_9001 crates (count, src, dst) =
  let src_stack = crates.(src) in
  let dst_stack = crates.(dst) in
  let to_move = List.take src_stack count in
  let remaining = List.drop src_stack count in
  crates.(src) <- remaining;
  crates.(dst) <- to_move @ dst_stack
;;

let apply_moves crates move_strat moves = List.iter moves ~f:(move_strat crates)

let read_top crates () =
  Array.map crates ~f:(fun l -> List.hd_exn l) |> Array.to_list |> String.of_char_list
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  (* part 1 *)
  let () =
    lines
    |> (List.map ~f:parse_move
       >> apply_moves crates move_9000
       >> read_top crates
       >> printf "\nPart 1: %s\n")
  in
  (* part 2. make sure to use duplicated copy of [crates]. *)
  let () =
    lines
    |> (List.map ~f:parse_move
       >> apply_moves crates_dup move_9001
       >> read_top crates_dup
       >> printf "Part 2: %s\n")
  in
  ()
;;
