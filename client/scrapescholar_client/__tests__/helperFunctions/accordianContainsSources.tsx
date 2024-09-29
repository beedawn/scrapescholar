import { render, screen, fireEvent, waitFor } from '@testing-library/react';

const accordianContainsSources = () =>{

        const scienceDirectChecklist = screen.getByText('ScienceDirect');
        const scopusChecklist = screen.getByText('Scopus');
        expect(scienceDirectChecklist).toBeInTheDocument();
        expect(scopusChecklist).toBeInTheDocument();
      
}


export default accordianContainsSources;