#!/usr/bin/python

import sys,os
import socket, struct

import pdb

ROOT_DB3_7 = "."
file_pre = "db3_7.pre.txt"
file_cur = "db3_7.cur.txt"

list_pre = []
list_cur = []
list_diff = []

filter_condition = {'country': 'us', 'state': 'ca', 'city': 'san francisco', 'metro_code': '807'}

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_pre = sys.argv[1]
        file_cur = sys.argv[2]

    for line in open(os.path.join(ROOT_DB3_7, file_pre)).readlines():
        items = line.strip().split(';')
        if len(items) != 10:
            print >>sys.stderr, 'line %s not handled' % line
            continue
        # ga("state");atlanta("city");broadband;524("metro_code");30349("postal_code");us("country");
        state, city, metro_code, postal_code, country = items[3], items[4], items[6], items[7], items[8]
        if country == filter_condition['country'] and state == filter_condition['state'] and city == filter_condition['city'] and metro_code == filter_condition['metro_code']:
            ip_left = items[0]
            ip_right = items[1]
            ip_left_int = struct.unpack("!L",socket.inet_aton(str(ip_left)))[0]
            ip_right_int = struct.unpack("!L",socket.inet_aton(str(ip_right)))[0]
            list_pre.append((ip_left_int, ip_right_int))


    for line in open(os.path.join(ROOT_DB3_7, file_cur)).readlines():
        items = line.strip().split(';')
        if len(items) != 10:
            print >>sys.stderr, 'line %s not handled' % line
            continue
        # ga("state");atlanta("city");broadband;524("metro_code");30349("postal_code");us("country");
        state, city, metro_code, postal_code, country = items[3], items[4], items[6], items[7], items[8]
        if country == filter_condition['country'] and state == filter_condition['state'] and city == filter_condition['city'] and metro_code == filter_condition['metro_code']:
            ip_left = items[0]
            ip_right = items[1]
            ip_left_int = struct.unpack("!L",socket.inet_aton(str(ip_left)))[0]
            ip_right_int = struct.unpack("!L",socket.inet_aton(str(ip_right)))[0]
            list_cur.append((ip_left_int, ip_right_int))
            if ip_left_int == -1 or ip_right_int == -1:
                print line

    ip_left = -1
    ip_right = -1
    i = 0
    j = 0
    while i < len(list_cur) and j < len(list_cur):
#        pdb.set_trace()
        if ip_left == -1:
            ip_left = list_cur[j][0]
            ip_right = list_cur[j][1]
            j += 1

        if ip_left < list_pre[i][0]:
            if ip_right < list_pre[i][0]:
                list_diff.append((ip_left, ip_right))
                ip_left = -1
            elif ip_right < list_pre[i][1]:
                list_diff.append((ip_left, list_pre[i][0]-1))
                ip_left = -1
            elif ip_right == list_pre[i][1]:
                list_diff.append((ip_left, list_pre[i][0]-1))
                ip_left = -1
                i += 1
            else:
                list_diff.append((ip_left, list_pre[i][0]-1))
                ip_left = list_pre[i][1] + 1
                i += 1
        elif ip_left <= list_pre[i][1]:
            if ip_right == list_pre[i][1]:
                ip_left = -1
                i += 1
            elif ip_right < list_pre[i][1]:
                ip_left = -1
            else:
                ip_left = list_pre[i][1] + 1
                i += 1
        else:
            i += 1

    for item in list_diff:
        print socket.inet_ntoa(struct.pack('!L', item[0])), ';', socket.inet_ntoa(struct.pack('!L', item[1]))
    if ip_left != -1:
        print socket.inet_ntoa(struct.pack('!L', ip_left)), ';', socket.inet_ntoa(struct.pack('!L', ip_right))



""">>> print ip
7.91.205.21
>>> print struct.unpack("!L",socket.inet_aton(str(ip)))[0]
123456789
>>> print (21+256*(205+256*(91+256*7)))
123456789
>>> print socket.inet_ntoa(struct.pack('!L', int_ip))
7.91.205.21
>>> print int_ip
123456789



1. logic
vector<pair(long, long)> vec_pre
vector<pair(long, long)> vec_cur
vector<pair(long, long)> vec_rst
long left = -1, right = -1;
long i, j;


while i < vec_pre.length && j < vec_cur.length:
    if left == -1:
        left = vec_cur.first
        right = vec_cur.second
        j += 1


    if left < vec_pre.first:
        if right < vec_pre.first:
            vec_rst.push_back(pair(left, right))
            left = -1
        if right < vec_pre.second:
            vec_rst.push_back(pair(left, vec_pre.first-1))
            left = -1
        else if right == vec_pre.second:
            vec_rst.push_back(pair(left, vec_pre.first-1))
            left = -1
            i += 1
        else
            vec_rst.push_back(pair(left, vec_pre.first-1))
            left = vec_pre.second + 1
            i += 1
    else if left <= vec_pre.second:
        if right == vec_pre.second:
            left = -1
            i += 1
        else if right < vec_pre.second:
            left = -1
        else:
            left = vec_pre.second + 1
            i += 1
    else:
        i += 1
        """
