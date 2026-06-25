from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = '激活指定的用户账户'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='要激活的用户名或邮箱'
        )

    def handle(self, *args, **options):
        username = options['username']
        User = get_user_model()

        try:
            # 尝试按用户名查找，如果失败则按邮箱查找
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.get(email=username)

            if user.is_active:
                self.stdout.write(
                    self.style.WARNING(f'用户 "{user.username}" 已经处于激活状态')
                )
            else:
                user.is_active = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'成功激活用户 "{user.username}"')
                )
        except User.DoesNotExist:
            raise CommandError(f'找不到用户: {username}')
