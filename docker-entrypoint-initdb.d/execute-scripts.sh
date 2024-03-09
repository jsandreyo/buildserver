######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

#!/bin/sh

echo "BUILD SERVER (remote): Changing to app directory..."
cd ../app

echo "BUILD SERVER (remote): Initializing up database..."
mysql -u root -p'D3v0p$2'< "buildserver-init-db.sql"
