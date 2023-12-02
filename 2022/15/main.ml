open Base
open Stdio

let make_range (xs, ys) (xb, yb) y =
  let dist = abs (xb - xs) + abs (yb - ys) in
  let dy = abs (y - ys) in
  let beacon = if y = yb then Some (xb, y) else None in
  if dy > dist
  then None
  else if dy = dist
  then (
    match beacon with
    | None -> None
    | _ -> Some ((xb, xb), beacon))
  else (
    let is_left = xs > xb in
    let dx = dist - dy in
    if is_left
    then
      Some
        ( (match beacon with
           | Some _ -> xs - dx + 1, xs + dx
           | None -> xs - dx, xs + dx)
        , beacon )
    else
      Some
        ( (match beacon with
           | Some _ -> xs - dx, xs + dx - 1
           | None -> xs - dx, xs + dx)
        , beacon ))
;;

let combine ranges =
  match ranges with
  | [] -> [ 0, 0 ]
  | hd :: tl ->
    let end', start =
      List.fold tl ~init:([], hd) ~f:(fun (inv_res, (ts, te)) (ns, ne) ->
        let nsvte = ns <= te + 1 in
        let tevne = te <= ne in
        match nsvte, tevne with
        | true, false -> inv_res, (ts, te)
        | true, true -> inv_res, (ts, ne)
        | false, _ -> (ts, te) :: inv_res, (ns, ne))
    in
    start :: end' |> List.rev
;;

let compare_points (a1, b1) (a2, b2) =
  let f = Int.compare a1 a2 in
  if f = 0 then Int.compare b1 b2 else f
;;

let preprocess raw_ranges =
  let ranges, beacons =
    List.fold
      (List.filter_map raw_ranges ~f:Fn.id)
      ~init:([], [])
      ~f:(fun (ranges, beacons) (range, beacon) ->
      ( range :: ranges
      , match beacon with
        | None -> beacons
        | Some b -> b :: beacons ))
  in
  let sorted_ranges = List.sort ranges ~compare:compare_points in
  let unique_beacons = List.dedup_and_sort beacons ~compare:compare_points in
  let beacons_x = List.map unique_beacons ~f:fst in
  let combined_ranges = combine sorted_ranges in
  combined_ranges, beacons_x
;;

let count_no_beacon ranges beacons =
  let n_beacons_in_ranges =
    List.fold beacons ~init:0 ~f:(fun count b ->
      if List.exists ranges ~f:(fun (x1, x2) -> x1 <= b && b <= x2)
      then count + 1
      else count)
  in
  let total_range_length =
    List.fold ranges ~init:0 ~f:(fun total (x1, x2) -> total + (x2 - x1 + 1))
  in
  total_range_length - n_beacons_in_ranges
;;

(* Part 2. *)
let make_range_include_beacon (xs, ys) (xb, yb) y =
  let dist = abs (xb - xs) + abs (yb - ys) in
  let dy = abs (y - ys) in
  let dx = dist - dy in
  if dy > dist then None else if dy = dist then Some (xb, xb) else Some (xs - dx, xs + dx)
;;

let get_raw_ranges input y =
  List.map input ~f:(fun (a, b) -> make_range_include_beacon a b y)
;;

let preprocess2 raw_ranges =
  let ranges = List.filter_map raw_ranges ~f:Fn.id in
  let sorted_ranges = List.sort ranges ~compare:compare_points in
  combine sorted_ranges
;;

let get_ranges input y = preprocess2 (get_raw_ranges input y)

let limited_ranges limit_start limit_end input y =
  let ranges = get_ranges input y |> List.filter ~f:(fun (x1, _) -> x1 <= limit_end) in
  let new_ranges =
    List.map ranges ~f:(fun (x1, x2) ->
      let a = x1 < limit_start in
      let b = x2 < limit_end in
      match a, b with
      | true, true -> limit_start, x2
      | true, false -> limit_start, limit_end
      | false, true -> x1, x2
      | false, false -> x1, limit_end)
  in
  new_ranges
;;

let tuning_frequency y ranges =
  let (_ : int), x2 = List.hd_exn ranges in
  let x = x2 + 1 in
  (x * 4000000) + y
;;

let result_part2 limit_start limit_end input =
  let y_list = List.init limit_end ~f:Fn.id in
  List.fold_until
    y_list
    ~init:0
    ~finish:(fun _ -> 0)
    ~f:(fun _ y ->
      let ranges = limited_ranges limit_start limit_end input y in
      if List.length ranges = 2 then Stop (tuning_frequency y ranges) else Continue 0)
;;

(* let input =
  [ (2, 18), (-2, 15)
  ; (9, 16), (10, 16)
  ; (13, 2), (15, 3)
  ; (12, 14), (10, 16)
  ; (10, 20), (10, 16)
  ; (14, 17), (10, 16)
  ; (8, 7), (2, 10)
  ; (2, 0), (2, 10)
  ; (0, 11), (2, 10)
  ; (20, 14), (25, 17)
  ; (17, 20), (21, 22)
  ; (16, 7), (15, 3)
  ; (14, 3), (15, 3)
  ; (20, 1), (15, 3)
  ]
;; *)

let input =
  [ (3772068, 2853720), (4068389, 2345925)
  ; (78607, 2544104), (-152196, 4183739)
  ; (3239531, 3939220), (3568548, 4206192)
  ; (339124, 989831), (570292, 1048239)
  ; (3957534, 2132743), (3897332, 2000000)
  ; (1882965, 3426126), (2580484, 3654136)
  ; (1159443, 3861139), (2580484, 3654136)
  ; (2433461, 287013), (2088099, -190228)
  ; (3004122, 3483833), (2580484, 3654136)
  ; (3571821, 799602), (3897332, 2000000)
  ; (2376562, 1539540), (2700909, 2519581)
  ; (785113, 1273008), (570292, 1048239)
  ; (1990787, 38164), (2088099, -190228)
  ; (3993778, 3482849), (4247709, 3561264)
  ; (3821391, 3986080), (3568548, 4206192)
  ; (2703294, 3999015), (2580484, 3654136)
  ; (1448314, 2210094), (2700909, 2519581)
  ; (3351224, 2364892), (4068389, 2345925)
  ; (196419, 3491556), (-152196, 4183739)
  ; (175004, 138614), (570292, 1048239)
  ; (1618460, 806488), (570292, 1048239)
  ; (3974730, 1940193), (3897332, 2000000)
  ; (2995314, 2961775), (2700909, 2519581)
  ; (105378, 1513086), (570292, 1048239)
  ; (3576958, 3665667), (3568548, 4206192)
  ; (2712265, 2155055), (2700909, 2519581)
  ]
;;

let () =
  let y = 2000000 in
  let raw_ranges = List.map input ~f:(fun (a, b) -> make_range a b y) in
  let ranges, beacons = preprocess raw_ranges in
  let ans = count_no_beacon ranges beacons in
  printf "\nPart 1: %d\n" ans
;;

let () = printf "Part 2: %d\n" (result_part2 0 4000000 input)
