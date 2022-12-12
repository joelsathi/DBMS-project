import { useState } from 'react';
import { Avatar, Button } from '@mui/material';

export default function ProfilePic() {
  const [isShown, setIsShown] = useState(false);

  return (
    <div className="App">
      <button
        onMouseEnter={() => setIsShown(true)}
        onMouseLeave={() => setIsShown(false)}>
            <Avatar
            alt="prfile picture"
            src="http://gavel.mrt.ac.lk/wp-content/uploads/2022/02/WhatsApp-Image-2022-02-06-at-8.17.07-PM-150x150.jpeg"
            sx={{
            height: 230,
            width: 180,
            boxShadow: 20,
            }}
            />
      </button>
      {isShown && (
        <div>
            <Button size="small" variant='outlined' color="inherit" sx={{ marginLeft: "auto" }}>Edit info</Button>  
        </div>
      )}
    </div>
  );
}

