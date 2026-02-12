import json
import time

def create_json(json_text):
    data = json.loads(json_text)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return data

def get_json():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def is_string(var):
    return isinstance(var, str)

def is_int(var):
    return isinstance(var, int)

def is_char(var):
    return (isinstance(var, str) and len(var) == 1) or var == ""

def is_stop_name(var):
    parts = var.split(" ")
    if len(parts) < 2:
        return False

    suffixes = ["Road", "Avenue", "Boulevard", "Street"]
    for word in suffixes:
        if word == parts[-1]:
            return True
    return False

def is_title(var):
    parts = var.split(" ")
    return parts[0] == parts[0].title()

def is_stop_type(var):
    if var in ["S", "O", "F"] or var == "":
        return True
    return False

def is_time_format(var):
    try:
        hour, minute = var.split(":")
        if len(hour) < 2:
            return False

        time.strptime(var, '%H:%M')
        return True
    except (ValueError, TypeError):
        return False

def check_data_type_reqs(json_text, errors):
    resolver = {
        "bus_id": is_int,
        "stop_id": is_int,
        "stop_name": is_string,
        "next_stop": is_int,
        "stop_type": is_char,
        "a_time": is_string
    }

    for obj in json_text:
        for key, value in obj.items():
            if not resolver[key](obj.get(key)):
                errors[key] += 1
            elif value == "" and key != "stop_type":
                errors[key] += 1
    return errors

def check_syntax(json_text, errors):
    for obj in json_text:
        for key, value in obj.items():
            if key == "stop_name" and (not is_title(value) or not is_stop_name(value)):
                errors[key] += 1
            elif key == "stop_type" and not is_stop_type(value):
                errors[key] += 1
            elif key == "a_time" and not is_time_format(value):
                errors[key] += 1
    return errors

def get_stop(json_text, target_value):
    stops = []
    for dic in json_text:
        if dic.get("bus_id") == target_value:
            stops.append(dic)
    return stops

def display_error_info(errors):
    total_errors = sum(errors.values())

    print(f"Type and field validation: {total_errors}")

    for error in errors:
        print(f"{error}: {errors[error]}")

def display_busline_info(json_text, bus_ids):
    print("Line names and number of stops:")
    for bus_id in bus_ids:
        num_stops = len(get_stop(json_text, bus_id))
        print(f"bus_id: {bus_id} stops: {num_stops}")

def get_unique_bus_ids(json_text):
    bus_ids = set()
    for dic in json_text:
        bus_id = dic.get("bus_id")
        if bus_id is not None:
            bus_ids.add(bus_id)
    return bus_ids

def is_attribute(var, bus_ids, json_text):
    is_found = False
    for id in bus_ids:
        for obj in json_text:
            if id == obj["bus_id"] and obj["stop_type"] == var:
                is_found = True
    return is_found

def check_stop_type(json_text, bus_id, stop_type):
    # Make sure each bus line has exactly one starting point (S) and one final stop (F).
    found_lst = []
    for obj in json_text:
        if obj["bus_id"] == bus_id and obj["stop_type"] == stop_type:
            found_lst.append(True)
        else:
            found_lst.append(False)
    return found_lst

def is_busses_complete(bus_ids, json_text):
    # print a message about it
    for id in bus_ids:
        flags = ["S", "F"]
        for flag in flags:
            found_lst = check_stop_type(json_text, id, flag)
            if not any(found_lst):
                return f"There is no start or end stop for the line: {id}"
    return None

def map_stop_types(json_text):
    stop_set = set()
    for obj in json_text:
        stop_set.add(obj["stop_type"])
    return stop_set

def get_street_names_by_type(json_text, stop_type):
    street_set = set()
    for obj in json_text:
        if obj["stop_type"] == stop_type:
            street_set.add(obj["stop_name"])
    return street_set

def display_stop_type_and_count(stops, label):
    print(f"{label} stops: {len(stops[label])} {sorted(stops[label])}")

def get_unique_street_names(json_text):
    return set(obj["stop_name"] for obj in json_text)

def map_street_names_count(street_names, json_text):
    name_to_count = {}

    for name in street_names:
        name_to_count[name] = 0

    for obj in json_text:
        name_to_count[obj["stop_name"]] += 1

    return name_to_count

def get_transfer_stops(json_text):
    street_names = get_unique_street_names(json_text)
    street_names_to_count = map_street_names_count(street_names, json_text)
    transfer_stops = []
    for key, value in street_names_to_count.items():
        if value > 1:
            transfer_stops.append(key)
    return transfer_stops

def get_on_demand_stops(json_text, s_stops, f_stops, t_stops):
    o_stops = get_street_names_by_type(json_text, "O")
    o_stops = o_stops.difference(s_stops)
    o_stops = o_stops.difference(f_stops)
    o_stops = o_stops.difference(t_stops)
    return o_stops

def check_time(json_text, bus_ids, errors):
    for bus_id in bus_ids:
        stops = get_stop(json_text, bus_id)
        for i in range(len(stops) - 1):
            if stops[i]["a_time"] > stops[i + 1]["a_time"]:
                errors["a_time"] += 1
                break

    return errors

def main():
    user_input = input()
    create_json(user_input)
    json_text = get_json()

    errors = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }
    bus_ids = get_unique_bus_ids(json_text)
    errors = check_time(json_text, bus_ids, errors)
    errors = check_data_type_reqs(json_text, errors)
    errors = check_syntax(json_text, errors)
    display_error_info(errors)
    print()

    display_busline_info(json_text, bus_ids)

    bus_status = is_busses_complete(bus_ids, json_text)
    if bus_status:
        print(bus_status)
    else:
        s_stops = get_street_names_by_type(json_text, "S")
        f_stops = get_street_names_by_type(json_text, "F")
        t_stops = get_transfer_stops(json_text)
        o_stops = get_on_demand_stops(json_text, s_stops, f_stops, t_stops)
        stops = {
            "Start": s_stops,
            "Finish": f_stops,
            "Transfer": t_stops,
            "On demand": o_stops,
        }

        display_stop_type_and_count(stops, "Start")
        display_stop_type_and_count(stops, "Transfer")
        display_stop_type_and_count(stops, "Finish")
        display_stop_type_and_count(stops, "On demand")

if __name__ == "__main__":
    main()
