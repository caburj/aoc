open Base
open Stdio

let ( >> ) g f x = f (g x)
let sort (a, b) = if a > b then b, a else a, b

let pair wall =
  let rec pair' wall res =
    match wall with
    | a :: b :: tl -> (a, b) :: pair' (b :: tl) res
    | _ -> []
  in
  pair' wall []
;;

let rec in_wall (x, y) wall =
  match wall with
  | (x1, y1) :: (x2, y2) :: tl ->
    let sx1, sx2 = sort (x1, x2) in
    let sy1, sy2 = sort (y1, y2) in
    (sx1 <= x && x <= sx2 && sy1 <= y && y <= sy2) || in_wall (x, y) ((x2, y2) :: tl)
  | _ -> false
;;

let in_walls walls (x, y) =
  List.fold walls ~init:false ~f:(fun acc wall -> acc || in_wall (x, y) wall)
;;

let is_blocked walls mound (x, y) =
  in_walls walls (x, y)
  || List.mem mound (x, y) ~equal:(fun (a, b) (c, d) -> a = c && b = d)
;;

let is_free walls mound = is_blocked walls mound >> not

let rec whiletrue pred func result =
  if pred result then whiletrue pred func (func result) else result
;;

let rec drop1 walls deepest mound sand =
  let x, y = sand in
  if y > deepest
  then mound, false
  else (
    let left_free = is_free walls mound (x - 1, y + 1) in
    let mid_free = is_free walls mound (x, y + 1) in
    let right_free = is_free walls mound (x + 1, y + 1) in
    match left_free, mid_free, right_free with
    | false, false, false -> sand :: mound, true
    | _, true, _ -> drop1 walls deepest mound (x, y + 1)
    | true, false, _ -> drop1 walls deepest mound (x - 1, y + 1)
    | false, false, true -> drop1 walls deepest mound (x + 1, y + 1))
;;

let rec drop2 walls deepest mound sand =
  let x, y = sand in
  if y >= deepest
  then sand :: mound, true
  else (
    let left_free = is_free walls mound (x - 1, y + 1) in
    let mid_free = is_free walls mound (x, y + 1) in
    let right_free = is_free walls mound (x + 1, y + 1) in
    match left_free, mid_free, right_free with
    | false, false, false -> sand :: mound, not (x = 500 && y = 0)
    | _, true, _ -> drop2 walls deepest mound (x, y + 1)
    | true, false, _ -> drop2 walls deepest mound (x - 1, y + 1)
    | false, false, true -> drop2 walls deepest mound (x + 1, y + 1))
;;

let parse input_lines =
  List.map input_lines ~f:(fun line ->
    String.split ~on:';' line
    |> List.map ~f:(fun str ->
         String.split ~on:',' str
         |> List.map ~f:Int.of_string
         |> function
         | [ a; b ] -> a, b
         | _ -> failwith ""))
;;

type entity =
  | Empty
  | Wall of string
  | Sand

let string_of_component = function
  | Empty -> "."
  | Wall x -> x
  | Sand -> "o"
;;

let bounds_of_mound mound =
  let min_x = List.fold mound ~init:Int.max_value ~f:(fun m (x, _) -> min m x) in
  let min_y = List.fold mound ~init:Int.max_value ~f:(fun m (_, y) -> min m y) in
  let max_x = List.fold mound ~init:Int.min_value ~f:(fun m (x, _) -> max m x) in
  let max_y = List.fold mound ~init:Int.min_value ~f:(fun m (_, y) -> max m y) in
  (min_x, min_y), (max_x, max_y)
;;

let draw walls mound =
  let min_x =
    List.fold walls ~init:Int.max_value ~f:(fun m ->
      List.fold ~init:m ~f:(fun m (x, _) -> min m x))
  in
  let min_y =
    List.fold walls ~init:Int.max_value ~f:(fun m ->
      List.fold ~init:m ~f:(fun m (_, y) -> min m y))
  in
  let max_x =
    List.fold walls ~init:Int.min_value ~f:(fun m ->
      List.fold ~init:m ~f:(fun m (x, _) -> max m x))
  in
  let max_y =
    List.fold walls ~init:Int.min_value ~f:(fun m ->
      List.fold ~init:m ~f:(fun m (_, y) -> max m y))
  in
  let (mmin_x, mmin_y), (mmax_x, mmax_y) = bounds_of_mound mound in
  let min_x = min min_x mmin_x in
  let min_y = min min_y mmin_y in
  let max_x = max max_x mmax_x in
  let max_y = max max_y mmax_y in
  let width = max_x - min_x + 1 in
  let height = max_y - min_y + 1 in
  let normalize (x, y) = x - min_x, y - min_y in
  let id_of_coord (nx, ny) = (ny * width) + nx in
  let normal_coord = normalize >> id_of_coord in
  let section = Array.create ~len:(width * height) Empty in
  let () =
    List.iter walls ~f:(fun wall ->
      List.iter (pair wall) ~f:(fun ((x1, y1), (x2, y2)) ->
        let same_x = x1 = x2 in
        let same_y = y1 = y2 in
        match same_x, same_y with
        | true, true -> failwith "should not happen"
        | false, false -> failwith "diagonal not allowed"
        | true, false ->
          let y1, y2 = sort (y1, y2) in
          section.(normal_coord (x1, y1)) <- Wall "+";
          section.(normal_coord (x1, y2)) <- Wall "+";
          for y = y1 + 1 to y2 - 1 do
            let id = normal_coord (x1, y) in
            section.(id) <- Wall "|"
          done
        | false, true ->
          let x1, x2 = sort (x1, x2) in
          section.(normal_coord (x1, y1)) <- Wall "+";
          section.(normal_coord (x2, y1)) <- Wall "+";
          for x = x1 + 1 to x2 - 1 do
            let id = normal_coord (x, y1) in
            section.(id) <- Wall "-"
          done))
  in
  let () =
    List.iter mound ~f:(fun (x, y) ->
      let id = normal_coord (x, y) in
      section.(id) <- Sand)
  in
  printf "\n";
  Array.iteri section ~f:(fun i c ->
    printf "%s" (string_of_component c);
    if (i + 1) % width = 0 then printf "\n" else ())
;;

let simulate ~debug drop walls deepest =
  let p (_, added) = added in
  let f (mound, _) = drop walls deepest mound (500, -1) in
  let f param =
    let m, x = f param in
    let () = if debug then draw walls m else () in
    m, x
  in
  fst (whiletrue p f ([], true))
;;

let () =
  let input_lines = In_channel.input_lines In_channel.stdin in
  let walls = parse input_lines in
  let deepest =
    List.fold walls ~init:0 ~f:(fun acc wall ->
      max acc (List.fold wall ~init:0 ~f:(fun m (_, y) -> max m y)))
  in
  let debug = false in
  let mound = simulate drop1 walls deepest ~debug in
  let () = if debug then draw walls mound else () in
  let () = printf "\nPart 1: %d\n" (List.length mound) in
  (* Part 2 took some time to run (maybe around 3mins).
     Maybe modeling the sand mound to be a set can help in the performance. *)
  let mound2 = simulate drop2 walls (deepest + 1) ~debug in
  let () = if debug then draw walls mound2 else () in
  let () = printf "Part 2: %d\n" (List.length mound2) in
  ()
;;
