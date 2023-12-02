open Base
open Stdio

type valve =
  { opened : bool
  ; rate : int
  ; adj : int list
  }

(* let network =
  [| { opened = false; rate = 17; adj = [ 32; 47; 61 ] }
   ; { opened = false; rate = 0; adj = [ 62; 31 ] }
   ; { opened = false; rate = 0; adj = [ 36; 18 ] }
   ; { opened = false; rate = 9; adj = [ 58; 52; 17; 38 ] }
   ; { opened = false; rate = 0; adj = [ 44; 62 ] }
   ; { opened = false; rate = 0; adj = [ 15; 37 ] }
   ; { opened = false; rate = 24; adj = [ 61; 25 ] }
   ; { opened = false; rate = 0; adj = [ 52; 36 ] }
   ; { opened = false; rate = 0; adj = [ 45; 34 ] }
   ; { opened = false; rate = 0; adj = [ 60; 17 ] }
   ; { opened = false; rate = 0; adj = [ 11; 44 ] }
   ; { opened = false; rate = 7; adj = [ 56; 54; 10; 19; 31 ] }
   ; { opened = false; rate = 0; adj = [ 51; 15 ] }
   ; { opened = false; rate = 0; adj = [ 43; 34 ] }
   ; { opened = false; rate = 20; adj = [ 40 ] }
   ; { opened = false; rate = 3; adj = [ 12; 43; 56; 5; 27 ] }
   ; { opened = false; rate = 0; adj = [ 42; 55 ] }
   ; { opened = false; rate = 0; adj = [ 9; 3 ] }
   ; { opened = false; rate = 0; adj = [ 50; 2 ] }
   ; { opened = false; rate = 0; adj = [ 11; 57 ] }
   ; { opened = false; rate = 0; adj = [ 59; 54 ] }
   ; { opened = false; rate = 0; adj = [ 48; 55 ] }
   ; { opened = false; rate = 0; adj = [ 39; 62 ] }
   ; { opened = false; rate = 0; adj = [ 35; 59 ] }
   ; { opened = false; rate = 0; adj = [ 34; 49 ] }
   ; { opened = false; rate = 0; adj = [ 46; 6 ] }
   ; { opened = false; rate = 0; adj = [ 53; 35 ] }
   ; { opened = false; rate = 0; adj = [ 15; 44 ] }
   ; { opened = false; rate = 0; adj = [ 36; 46 ] }
   ; { opened = false; rate = 0; adj = [ 50; 33 ] }
   ; { opened = false; rate = 0; adj = [ 41; 44 ] }
   ; { opened = false; rate = 0; adj = [ 1; 11 ] }
   ; { opened = false; rate = 0; adj = [ 0; 55 ] }
   ; { opened = false; rate = 0; adj = [ 29; 46 ] }
   ; { opened = false; rate = 0; adj = [ 8; 24; 13; 57; 39 ] }
   ; { opened = false; rate = 11; adj = [ 37; 42; 23; 49; 26 ] }
   ; { opened = false; rate = 14; adj = [ 28; 2; 7 ] }
   ; { opened = false; rate = 0; adj = [ 5; 35 ] }
   ; { opened = false; rate = 0; adj = [ 50; 3 ] }
   ; { opened = false; rate = 0; adj = [ 22; 34 ] }
   ; { opened = false; rate = 0; adj = [ 47; 14 ] }
   ; { opened = false; rate = 0; adj = [ 30; 55 ] }
   ; { opened = false; rate = 0; adj = [ 16; 35 ] }
   ; { opened = false; rate = 0; adj = [ 15; 13 ] }
   ; { opened = false; rate = 6; adj = [ 45; 4; 27; 10; 30 ] }
   ; { opened = false; rate = 0; adj = [ 8; 44 ] }
   ; { opened = false; rate = 21; adj = [ 33; 28; 25 ] }
   ; { opened = false; rate = 0; adj = [ 40; 0 ] }
   ; { opened = false; rate = 0; adj = [ 21; 50 ] }
   ; { opened = false; rate = 0; adj = [ 35; 24 ] }
   ; { opened = false; rate = 8; adj = [ 38; 48; 29; 18 ] }
   ; { opened = false; rate = 0; adj = [ 12; 62 ] }
   ; { opened = false; rate = 0; adj = [ 7; 3 ] }
   ; { opened = false; rate = 0; adj = [ 26; 62 ] }
   ; { opened = false; rate = 0; adj = [ 11; 20 ] }
   ; { opened = false; rate = 13; adj = [ 16; 41; 32; 21; 58 ] }
   ; { opened = false; rate = 0; adj = [ 11; 15 ] }
   ; { opened = false; rate = 0; adj = [ 19; 34 ] }
   ; { opened = false; rate = 0; adj = [ 55; 3 ] }
   ; { opened = false; rate = 15; adj = [ 20; 23 ] }
   ; { opened = false; rate = 25; adj = [ 9 ] }
   ; { opened = false; rate = 0; adj = [ 6; 0 ] }
   ; { opened = false; rate = 5; adj = [ 22; 1; 51; 4; 53 ] }
  |]
;; *)

let sample_network =
  [| { opened = false; rate = 0; adj = [ 3; 8; 1 ] }
   ; { opened = false; rate = 13; adj = [ 2; 0 ] }
   ; { opened = false; rate = 2; adj = [ 3; 1 ] }
   ; { opened = false; rate = 20; adj = [ 2; 0; 4 ] }
   ; { opened = false; rate = 3; adj = [ 5; 3 ] }
   ; { opened = false; rate = 0; adj = [ 4; 6 ] }
   ; { opened = false; rate = 0; adj = [ 5; 7 ] }
   ; { opened = false; rate = 22; adj = [ 6 ] }
   ; { opened = false; rate = 0; adj = [ 0; 9 ] }
   ; { opened = false; rate = 21; adj = [ 8 ] }
  |]
;;

(* let coord_of_id m id = id / m, id % m *)
let id_of_coord m (i, j) = (i * m) + j
let ( >> ) g f x = f (g x)
let pow_2 = Int.shift_left 1

let bool_array_to_int =
  Array.foldi ~init:0 ~f:(fun i acc b -> acc + if b then pow_2 i else 0)
;;

let int_to_bool_array len n =
  Array.create ~len false
  |> Array.fold ~init:([], n) ~f:(fun (l, n) _ ->
       let q, r = n / 2, n % 2 in
       (r = 1) :: l, q)
  |> fst
  |> Array.of_list
;;

let network_config =
  Array.filter ~f:(fun valve -> valve.rate > 0)
  >> Array.map ~f:(fun valve -> valve.opened)
  >> bool_array_to_int
;;

let network_of_config network config =
  let network_copy = Array.copy network in
  let has_flow_rates =
    Array.mapi network ~f:(fun i v -> i, v)
    |> Array.filter ~f:(fun (_, v) -> v.rate > 0)
    |> Array.map ~f:fst
  in
  let ba = int_to_bool_array (Array.length has_flow_rates) config in
  let () =
    Array.iteri has_flow_rates ~f:(fun i v_id ->
      if ba.(i)
      then network_copy.(v_id) <- { (network.(v_id)) with opened = true }
      else ())
  in
  network_copy
;;

let list_max l =
  List.fold
    ~init:(List.hd_exn l)
    ~f:(fun (x, nx) (y, ny) -> if x > y then x, nx else y, ny)
    l
;;

let max_pressure time_limit orig_network start_valve_id =
  let n_network_config =
    1
    + (orig_network
      |> (Array.filter ~f:(fun valve -> valve.rate > 0)
         >> Array.length
         >> (fun len -> Array.create ~len true)
         >> bool_array_to_int))
  in
  let cache =
    Array.make_matrix
      ~dimx:(Array.length orig_network * (time_limit + 1))
      ~dimy:n_network_config
      (-1, -1)
  in
  let rec max_pressure' time_limit (network, time, valve_id) =
    let config = network_config network in
    let index = id_of_coord time_limit (valve_id, time) in
    let cached = cache.(index).(config) in
    if fst cached <> -1
    then cached
    else (
      let temp =
        if time = time_limit || Array.for_all network ~f:(fun valve -> valve.opened)
        then 0, config
        else (
          let valve = network.(valve_id) in
          let check_adj =
            List.map valve.adj ~f:(fun av_id ->
              let my_mp, my_config =
                max_pressure' time_limit (network, time + 1, av_id)
              in
              let el_mp, el_config =
                max_pressure'
                  time_limit
                  (network_of_config network my_config, time + 1, av_id)
              in
              my_mp + el_mp, el_config)
          in
          if valve.rate = 0 || valve.opened
          then check_adj |> list_max
          else (
            let updated_network =
              Array.mapi network ~f:(fun i v ->
                if i = valve_id then { valve with opened = true } else v)
            in
            let added_pressure = (time_limit - (time + 1)) * valve.rate in
            let max_p_by_opening, no =
              max_pressure' time_limit (updated_network, time + 1, valve_id)
            in
            let max_p_by_opening_el, el_config =
              max_pressure'
                time_limit
                (network_of_config updated_network no, time + 1, valve_id)
            in
            (max_p_by_opening + added_pressure + max_p_by_opening_el, el_config)
            :: check_adj
            |> list_max))
      in
      cache.(index).(config) <- temp;
      temp)
  in
  max_pressure' time_limit (orig_network, 0, start_valve_id)
;;

let () =
  let mp, x = max_pressure 20 sample_network 0 (* Sample AA is 0 *) in
  let () = printf "\nPart 1 (sample): %d\n" mp in
  let () =
    printf
      "opened valves: %s\n"
      (network_of_config sample_network x
      |> Array.map ~f:(fun v -> v.opened)
      |> Array.sexp_of_t Bool.sexp_of_t
      |> Sexp.to_string)
  in
  let mp_by_me, n = max_pressure 26 sample_network 0 in
  let () = printf "opened valves: %d\n" n in
  let mp_by_elephant, _ = max_pressure 26 sample_network 0 in
  let () =
    printf
      "Part 2 (sample): me = %d, elephant = %d, total = %d\n"
      mp_by_me
      mp_by_elephant
      (mp_by_me + mp_by_elephant)
  in
  ()
;;

(* let () =
  let mp, _ = max_pressure 30 network 34 (* AA is 34 *) in
  printf "Part 1: %d\n" mp
;; *)
