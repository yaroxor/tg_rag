.messages as $messages | ( [ $messages[] | keys[] ] | unique ) as $keys | reduce $keys[] as $key ( {}; .[$key] = [ $messages[] | select(has($key)) | .[$key] ] ) | map_values(unique)
