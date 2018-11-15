#!/usr/bin/env bash
find ./ | grep "[.]py$" | grep -v old | xargs cat | grep import | sort | uniq | grep -v 'from [.]' | cut -f2 -d\   | cut -f1 -d. | sort | uniq
