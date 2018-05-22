import React, { Component } from 'react'
import Footer from '../ui/Footer';
import ModalAbout from '../ui/ModalAbout';
import ModalContact from '../ui/ModalContact';

export default class FinalPage extends Component {

    render() {
        return (
            <div>
                <ModalAbout />
                <ModalContact />
                <Footer />
            </div>
        );
    }
}