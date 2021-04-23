# Experiment with two tcp flows going through two different routers
#
# $Id: config-two-routers.py,v 9528f837a557 2016/06/06 03:37:45 s_zander $

import sys
import datetime
from fabric.api import env


#
# Fabric config
#

# User and password
env.user = 'root'
env.password = 'johnday'

# Set shell used to execute commands
env.shell = '/bin/sh -c'

#
# Testbed config
#

# Path to teacup scripts
TPCONF_script_path = '/home/ocarina/kristjoc/teacup/teacup-1.1'
# DO NOT remove the following line
sys.path.append(TPCONF_script_path)

# Set debugging level (0 = no debugging info output)
TPCONF_debug_level = 0

# Host lists
TPCONF_router = ['hylia', 'midna']
TPCONF_hosts = ['zelda', 'majora']

# Map external IPs to internal IPs
TPCONF_host_internal_ip = {
    'hylia': ['10.100.110.3', '10.100.120.3'],
    'midna':  ['10.100.120.6', '10.100.130.6'],
    'zelda':  ['10.100.110.2'],
    'majora':  ['10.100.130.7'],
}

TPCONF_check_connectivity = '0'

# Time offset measurement options
# Enable broadcast ping on external/control interfaces
TPCONF_bc_ping_enable = '1'

# Specify rate of pings in packets/second
TPCONF_bc_ping_rate = 1

# Specify multicast address to use (must be broadcast or multicast address)
# If this is not specified, byt deafult the ping will be send to the subnet
# broadcast address.
TPCONF_bc_ping_address = '224.0.1.199'

# Specify the poll interval for web10g data logging in millieseconds (smallest
# supported value is currently 1ms). This is used for web10g on Linux as well
# as the EStats logger on Windows. The default value is 10ms.
TPCONF_web10g_poll_interval = 1

# Specify type of TCP logger used on Linux. The value can be 'web10g',
# 'ttprobe' or 'both', where 'both' means both web10g and ttprobe are used.
# The value can only be set to 'ttprobe' or 'both' if ttprobe is installed
# (see http://caia.swin.edu.au/tools/teacup/downloads.html)
TPCONF_linux_tcp_logger = 'web10g'

#
# Reboot configuration
#

# Experiment settings
#

# Maximum allowed time difference between machines in seconds
# otherwise experiment will abort cause synchronisation problems
TPCONF_max_time_diff = 2

# Experiment name prefix used if not set on the command line
# The command line setting will overrule this config setting
now = datetime.datetime.today()
# new default test ID prefix
TPCONF_test_id = 'exp_' + now.strftime("%Y%m%d-%H%M%S")

# Directory to store log files on remote host
TPCONF_remote_dir = '/tmp/'

#
# List of router queues/pipes
#

# Each entry is a tuple. The first value is the queue number and the second value
# is a comma separated list of parameters (see routersetup.py:init_pipe()).
# Queue numbers must be unique.

# Note that variable parameters must be either constants or or variable names
# defined by the experimenter. Variables are evaluated during runtime. Variable
# names must start with a 'V_'. Parameter names can only contain numbes, letter
# (upper and lower case), underscores (_), and hypen/minus (-).

# All variables must be defined in TPCONF_variable_list (see below).

# Note parameters must be configured appropriately for the router OS, e.g. there
# is no CoDel on FreeBSD; otherwise the experiment will abort witn an error.

hylia_queues = [
    # Set same delay for every host
    ('1', " source='10.100.110.0/24', dest='10.100.130.0/24', delay=V_delay, "
     " loss=V_loss, rate=V_up_rate, queue_disc=V_aqm, queue_size=V_bsize, "
     " queue_disc_params=V_aqm_param "),
    ('2', " source='10.100.130.0/24', dest='10.100.110.0/24', delay=V_delay, "
     " loss=V_loss, rate=V_down_rate, queue_disc=V_aqm, queue_size=V_bsize, "
     " queue_disc_params=V_aqm_param "),
]

midna_queues = [
    # Set same delay for every host
    ('1', " source='10.100.110.0/24', dest='10.100.130.0/24', delay=V_delay, "
     " loss=V_loss, rate=V_up_rate, queue_disc=V_aqm, queue_size=V_bsize, "
     " queue_disc_params=V_aqm_param "),
    ('2', " source='10.100.130.0/24', dest='10.100.110.0/24', delay=V_delay, "
     " loss=V_loss, rate=V_down_rate, queue_disc=V_aqm, queue_size=V_bsize, "
     " queue_disc_params=V_aqm_param "),
]


TPCONF_router_queues = {}
TPCONF_router_queues['hylia'] = hylia_queues
TPCONF_router_queues['midna'] = midna_queues

#
# List of traffic generators
#

# Each entry is a 3-tuple. the first value of the tuple must be a float and is the
# time relative to the start of the experiment when tasks are excuted. If two tasks
# have the same start time their start order is arbitrary. The second entry of the
# tuple is the task number and  must be a unique integer (used as ID for the process).
# The last value of the tuple is a comma separated list of parameters (see the tasks
# defined in trafficgens.py); the first parameter of this list must be the
# task name.

# Client and server can be specified using the external/control IP addresses or host
# names. Then the actual interface used is the _first_ internal address (according to
# TPCONF_host_internal_ip). Alternativly, client and server can be specified as
# internal addresses, which allows to use any internal interfaces configured.

traffic_iperf = [
    # Specifying external addresses traffic will be created using the _first_
    # internal addresses (according to TPCONF_host_internal_ip)
    ('0.0', '1', " start_iperf, client='zelda', server='majora', port=5000, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '2', " start_iperf, client='zelda', server='majora', port=5001, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '3', " start_iperf, client='zelda', server='majora', port=5003, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '4', " start_iperf, client='zelda', server='majora', port=5004, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '5', " start_iperf, client='zelda', server='majora', port=5005, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '6', " start_iperf, client='zelda', server='majora', port=5006, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '7', " start_iperf, client='zelda', server='majora', port=5007, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '8', " start_iperf, client='zelda', server='majora', port=5008, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '9', " start_iperf, client='zelda', server='majora', port=5009, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
    ('0.0', '10', " start_iperf, client='zelda', server='majora', port=5010, "
     " duration=V_duration, bandw=100M, buf_size=262144 "),
]

# THIS is the traffic generator setup we will use
TPCONF_traffic_gens = traffic_iperf

#
# Traffic parameters
#

# Duration in seconds of traffic
TPCONF_duration = 10

# Number of runs for each setting
TPCONF_runs = 1

# If '1' enable ecn for all hosts, if '0' disable ecn for all hosts
TPCONF_ECN = ['0', '1']

# TCP congestion control algorithm used
# Possible algos are: default, host<N>, newreno, cubic, cdg, hd, htcp, compound, vegas
# Note that the algo support is OS specific, so must ensure the right OS is booted
# Windows: newreno (default), compound
# FreeBSD: newreno (default), cubic, hd, htcp, cdg, vegas
# Linux: newreno, cubic (default), htcp, vegas
# Mac: newreno
# If you specify 'default' the default algorithm depending on the OS will be used
# If you specify 'host<N>' where <N> is an integer starting from 0 to then the
# algorithm will be the N-th algorithm specified for the host in TPCONF_host_TCP_algos
# (in case <N> is larger then the number of algorithms specified, it is set to 0
TPCONF_TCP_algos = ['reno', 'dctcp', 'lgc', ]

# Specify TCP congestion control algorithms used on each host
TPCONF_host_TCP_algos = {
}

# Specify TCP parameters for each host and each TCP congestion control algorithm
# Each parameter is of the form <sysctl name> = <value> where <value> can be a constant
# or a V_ variable
TPCONF_host_TCP_algo_params = {
}

# Specify arbitray commands that are executed on a host at the end of the host
# intialisation (after general host setup, ecn and tcp setup). The commands are
# executed in the shell as written after any V_ variables have been replaced.
# LIMITATION: only one V_ variable per command
TPCONF_host_init_custom_cmds = {
    'zelda' : ['echo 3020 | sudo tee /sys/module/tcp_lgc/parameters/lgc_logPhi_scaled',
               'echo 16384 | sudo tee /sys/module/tcp_lgc/parameters/lgc_alpha_scaled',
               'echo 22051 | sudo tee /sys/module/tcp_lgc/parameters/lgc_logP_scaled',
               'echo 20 | sudo tee /sys/module/tcp_lgc/parameters/lgc_coef',
               'echo 12500 | sudo tee /sys/module/tcp_lgc/parameters/lgc_max_rate = 12500'],
    'majora' : ['echo 3020 | sudo tee /sys/module/tcp_lgc/parameters/lgc_logPhi_scaled',
                'echo 16384 | sudo tee /sys/module/tcp_lgc/parameters/lgc_alpha_scaled',
                'echo 22051 | sudo tee /sys/module/tcp_lgc/parameters/lgc_logP_scaled',
                'echo 20 | sudo tee /sys/module/tcp_lgc/parameters/lgc_coef',
                'echo 12500 | sudo tee /sys/module/tcp_lgc/parameters/lgc_max_rate = 12500'],
}

# Emulated delays in ms
TPCONF_delays = [5]

# Emulated loss rates
TPCONF_loss_rates = [0]

# Emulated bandwidths (downstream, upstream)
TPCONF_bandwidths = [
    ('50mbit', '100mbit'),
]

# AQM
# Linux: fifo (mapped to pfifo), pfifo, bfifo, fq_codel, codel, pie, red, ...
#        (see tc man page for full list)
# FreeBSD: fifo, red
TPCONF_aqms = ['shq', 'red', 'pfifo']

# Buffer size
# If router is Linux this is mostly in packets/slots, but it depends on AQM
# (e.g. for bfifo it's bytes)
# If router is FreeBSD this would be in slots by default, but we can specify byte sizes
# (e.g. we can specify 4Kbytes)
TPCONF_buffer_sizes = [1000]

TPCONF_aqms_params = ['interval 10ms maxp 0.02 alpha 0.25 bandwidth 100mbit ecn',
                      'min 30000 max 90000 avpkt 1000 burst 50 bandwidth 100mbit probability 0.02 ecn']
#
# List of all parameters that can be varied and default values
#

# The key of each item is the identifier that can be used in TPCONF_vary_parameters
# (see below).
# The value of each item is a 4-tuple. First, a list of variable names.
# Second, a list of short names uses for the file names.
# For each parameter varied a string '_<short_name>_<value>' is appended to the log
# file names (appended to chosen prefix). Note, short names should only be letters
# from a-z or A-Z. Do not use underscores or hyphens!
# Third, the list of parameters values. If there is more than one variable this must
# be a list of tuples, each tuple having the same number of items as teh number of
# variables. Fourth, an optional dictionary with additional variables, where the keys
# are the variable names and the values are the variable values.

TPCONF_parameter_list = {
#   Vary name		V_ variable	  file name	values			extra vars
    'ecns' 	    :  (['V_ecn'],	  ['ecn'], 	TPCONF_ECN, 		 {}),
    'delays' 	    :  (['V_delay'], 	  ['del'], 	TPCONF_delays, 		 {}),
    'loss'  	    :  (['V_loss'], 	  ['loss'], 	TPCONF_loss_rates, 	 {}),
    'tcpalgos' 	    :  (['V_tcp_cc_algo'],['tcp'], 	TPCONF_TCP_algos, 	 {}),
    'aqms'	    :  (['V_aqm'], 	  ['aqm'], 	TPCONF_aqms, 		 {}),
    'aqms_params'   :  (['V_aqm_param'],  ['aqm_param'],TPCONF_aqms_params, 	 {}),
    'bsizes'	    :  (['V_bsize'], 	  ['bs'], 	TPCONF_buffer_sizes, 	 {}),
    'runs'	    :  (['V_runs'],       ['run'], 	range(TPCONF_runs), 	 {}),
    'bandwidths'    :  (['V_down_rate', 'V_up_rate'], ['down', 'up'], TPCONF_bandwidths, {}),
}

# Default setting for variables (used for variables if not varied)

# The key of each item is the parameter  name. The value of each item is the default
# parameter value used if the variable is not varied.

TPCONF_variable_defaults = {
#   V_ variable			value
    'V_ecn'  		:	TPCONF_ECN[1],
    'V_duration'  	:	TPCONF_duration,
    'V_delay'  		:	TPCONF_delays[0],
    'V_loss'   		:	TPCONF_loss_rates[0],
    'V_tcp_cc_algo' 	:	TPCONF_TCP_algos[2],
    'V_down_rate'   	:	TPCONF_bandwidths[0][0],
    'V_up_rate'	    	:	TPCONF_bandwidths[0][1],
    'V_aqm'	    	:	TPCONF_aqms[0],
    'V_aqm_param'	:	TPCONF_aqms_params[0],
    'V_bsize'	    	:	TPCONF_buffer_sizes[0],
}

# Specify the parameters we vary through all values, all others will be fixed
# according to TPCONF_variable_defaults
TPCONF_vary_parameters = ['tcpalgos', 'delays', 'bandwidths', 'aqms', 'runs']
