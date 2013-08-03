from base import Task
from common import phases
import os.path


class EnableShadowConfig(Task):
	description = 'Enabling shadowconfig'
	phase = phases.system_modification

	def run(self, info):
		from common.tools import log_check_call
		log_check_call(['/usr/sbin/chroot', info.root, '/sbin/shadowconfig', 'on'])

class SetRootPassword(Task):
	description = 'Set password for root'
	phase = phases.system_modification

	def run(self, info):
		from common.tools import log_check_call
		if info.manifest.credentials['root']:
			log_check_call(['/usr/sbin/chroot', info.root, '/usr/sbin/chpasswd'], 'root:'+info.manifest.credentials['root'])

class DisableSSHPasswordAuthentication(Task):
	description = 'Disabling SSH password authentication'
	phase = phases.system_modification

	def run(self, info):
		from common.tools import sed_i
		if 'root' not in info.manifest.credentials:
			# If no password set for root
			sshd_config_path = os.path.join(info.root, 'etc/ssh/sshd_config')
			sed_i(sshd_config_path, '^#PasswordAuthentication yes', 'PasswordAuthentication no')


class DisableSSHDNSLookup(Task):
	description = 'Disabling sshd remote host name lookup'
	phase = phases.system_modification

	def run(self, info):
		sshd_config_path = os.path.join(info.root, 'etc/ssh/sshd_config')
		with open(sshd_config_path, 'a') as sshd_config:
			sshd_config.write('UseDNS no')