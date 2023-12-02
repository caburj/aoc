open Base
open Stdio

type packet =
  | Base of int
  | Nested of packet list

let rec compare a b =
  match a with
  | Base i ->
    (match b with
    | Base j -> Int.compare i j
    | Nested _ -> compare (Nested [ Base i ]) b)
  | Nested la ->
    (match b with
    | Base _ -> neg (compare b a)
    | Nested lb ->
      let na = List.length la in
      let nb = List.length lb in
      let n = min na nb in
      let ha = List.take la n in
      let hb = List.take lb n in
      let pairs = List.zip_exn ha hb in
      let unequal_pairs = List.drop_while ~f:(fun (a, b) -> compare a b = 0) pairs in
      (match unequal_pairs with
      | [] -> Int.compare na nb
      | (a, b) :: _ -> compare a b))
;;

(* Learned here some concept of look-ahead. *)
let rec tokenize chars result =
  match chars with
  | a :: atl ->
    (match a with
    | ',' -> tokenize atl result
    | '1' ->
      (match atl with
      | b :: btl ->
        if Char.( = ) b '0'
        then "10" :: tokenize btl result
        else "1" :: tokenize atl result
      | [] -> "1" :: result)
    | _ -> String.of_char a :: tokenize atl result)
  | [] -> result
;;

(* There's gotta be a better way of parsing the string than this! *)
let parse str =
  let tokens = tokenize (String.to_list str) [] in
  let rec make_packet tokens stack =
    match tokens with
    | "[" :: tl -> make_packet tl (Nested [] :: stack)
    | "]" :: tl ->
      (match stack with
      | a :: b :: bottom ->
        (match b with
        | Nested l -> make_packet tl (Nested (l @ [ a ]) :: bottom)
        | _ -> failwith "not gonna happen")
      | [ a ] -> a
      | _ -> failwith "not gonna happen")
    | x :: tl ->
      (match stack with
      | top :: bottom ->
        (match top with
        | Nested l -> make_packet tl (Nested (l @ [ Base (Int.of_string x) ]) :: bottom)
        | _ -> failwith "not gonna happen")
      | [] -> failwith "not gonna happen")
    | [] -> failwith "not gonna happen"
  in
  make_packet tokens []
;;

let () =
  let input_lines =
    In_channel.input_lines In_channel.stdin
    |> List.filter ~f:(fun x -> String.( <> ) x "")
  in
  let rec make_pairs input_lines =
    match input_lines with
    | a :: b :: tl -> (a, b) :: make_pairs tl
    | [] -> []
    | _ -> failwith "not gonna happen hopefully"
  in
  let str_pairs = make_pairs input_lines in
  let comparisons =
    List.map str_pairs ~f:(fun (str_left, str_right) ->
        let left = parse str_left in
        let right = parse str_right in
        compare left right)
  in
  let indeces =
    List.filter_mapi comparisons ~f:(fun i x -> if x < 0 then Some (i + 1) else None)
  in
  let sum_indeces = List.fold indeces ~init:0 ~f:( + ) in
  let () = printf "\nPart 1: %d\n" sum_indeces in
  (* For part 2 *)
  let augmented_lines = "[[2]]" :: "[[6]]" :: input_lines in
  let indexed_packets = List.mapi augmented_lines ~f:(fun i line -> i, parse line) in
  let compare' (_, a) (_, b) = compare a b in
  let sorted_packets = List.sort ~compare:compare' indexed_packets in
  let f = List.length (List.take_while sorted_packets ~f:(fun (i, _) -> i <> 0)) + 1 in
  let s = List.length (List.take_while sorted_packets ~f:(fun (i, _) -> i <> 1)) + 1 in
  let () = printf "Part 2: %d\n" (f * s) in
  ()
;;
