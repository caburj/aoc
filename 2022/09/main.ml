open Base
open Stdio

module Coord = struct
  module T = struct
    type t = int * int

    let compare (x1, y1) (x2, y2) =
      let cmp_x = Int.compare x1 x2 in
      if cmp_x <> 0 then cmp_x else Int.compare y1 y2
    ;;

    let sexp_of_t (x, y) : Sexp.t =
      List [ Atom (Int.to_string x); Atom (Int.to_string y) ]
    ;;
  end

  include T
  include Comparator.Make (T)
end

let ( >> ) g f x = f (g x)

let follow_front (fx, fy) (bx, by) =
  (* These conditions are added for part 2. Front can now move diagonally. *)
  if fx = bx + 2 && fy = by + 2
  then bx + 1, by + 1
  else if fx = bx + 2 && fy = by - 2
  then bx + 1, by - 1
  else if fx = bx - 2 && fy = by - 2
  then bx - 1, by - 1
  else if fx = bx - 2 && fy = by + 2
  then bx - 1, by + 1
  (* From Part 1. The head (Front) can only move right, left, up, down. *)
  else if fx = bx + 2 (* Front is at right of Back *)
  then bx + 1, fy
  else if fx = bx - 2 (* Front is at left of Back *)
  then bx - 1, fy
  else if fy = by + 2 (* Front is on top of Back *)
  then fx, by + 1
  else if fy = by - 2 (* Front is below of Back *)
  then fx, by - 1
  else bx, by
;;

let follow_head hd tl =
  hd
  :: List.folding_map tl ~init:hd ~f:(fun prev t ->
         let newt = follow_front prev t in
         newt, newt)
;;

let move_right (hx, hy) tail = follow_head (hx + 1, hy) tail
let move_up (hx, hy) tail = follow_head (hx, hy + 1) tail
let move_down (hx, hy) tail = follow_head (hx, hy - 1) tail
let move_left (hx, hy) tail = follow_head (hx - 1, hy) tail

let move rope instruction =
  match rope with
  | head :: tail ->
    (match instruction with
    | "R" -> move_right head tail
    | "U" -> move_up head tail
    | "D" -> move_down head tail
    | "L" -> move_left head tail
    | _ -> failwith "instruction not supported")
  | _ -> failwith "impossible empty rope"
;;

let init_tail_positions t = Set.of_list (module Coord) [ t ]

let count_t_visited rope instructions =
  let tail = List.last_exn rope in
  instructions
  |> (List.fold
        ~init:(init_tail_positions tail, rope)
        ~f:(fun (tpos, prev_rope) instruction ->
          let moved_rope = move prev_rope instruction in
          Set.add tpos (List.last_exn moved_rope), moved_rope)
     >> fst
     >> Set.length)
;;

let parse_instructions lines =
  List.map lines ~f:(fun line ->
      String.split ~on:' ' line
      |> function
      | [ a; b ] -> a, Int.of_string b
      | _ -> failwith "not gonna happen")
  |> List.fold ~init:[] ~f:(fun acc (sym, n) -> acc @ List.init n ~f:(fun _ -> sym))
;;

let () =
  let lines = In_channel.input_lines In_channel.stdin in
  let instructions = parse_instructions lines in
  printf "\nPart 1: %d\n" (count_t_visited (List.init 2 ~f:(fun _ -> 0, 0)) instructions);
  printf "Part 2: %d\n" (count_t_visited (List.init 10 ~f:(fun _ -> 0, 0)) instructions)
;;
